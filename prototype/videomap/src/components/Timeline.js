import React, { useState, useEffect, useRef } from "react"
import { Tooltip, Box } from "@material-ui/core";
import { labelInfo } from "../labelInfo";

import './Timeline.css';
import pinImage from './../image/custom_pin.png';


function LabelBox ({
    item, 
    colorPalette, 
    duration, 
    position, 
    setVideoTime, 
    setPosition,  
    video, 
    videoTime, 
    logData,
    showLabelInfo,
    hideLabelInfo,
    setSelectedIndex
}) {

    const calWidth = (start, end) => {
        var width = (end-start)/duration*850;
        return width;
    } 

    const posToTime = (pos) => {
        var time = pos * duration / 850;
        var min = (Math.floor(time /  60)).toString();
        var sec = (Math.floor(time - min * 60)).toString();
        if (sec.length == 1) {
          sec = 0 + sec;
        }
        return min + ':' + sec;  
    }
  
    const handleMouseMove = (event) => {
        setPosition(event.clientX - 300);
    };

    const handleTimelineClick = (item) =>{
        if (!item.use) return false;

        const newTime = (position * duration / 850).toFixed(3);
        // logging
        const video_timestamp = {
            from: videoTime,
            to: newTime
        }
        const meta = {
            source: "mouse", 
            location: "timeline",
            low_label: item.low_label,
            high_label: item.high_label 
        };
        logData ("jump", video_timestamp, meta);

        video.seekTo (newTime);
    }

    const updateHoverLabel = (label) => {
        // if (!label){
        //     setHoverLabel("");
        // }
        // else {
        //     setHoverLabel(label);
        // }
    }

    return (
        <div 
            className="label_box" 
            onClick={()=>handleTimelineClick(item)} 
            onMouseMove={(e)=>handleMouseMove(e)} 
            onMouseEnter={() => showLabelInfo(item.low_label)} 
            onMouseLeave={() => hideLabelInfo(item.low_label)} 
            style={{width: calWidth(item.start, item.next_start), height: "20px", backgroundColor: item.use ? colorPalette[item.low_label] : "white", cursor: !item.use && "default" }}
        >
            <span className="tooltiptext">{item.low_label}<br/>{posToTime(position)}</span>   
        </div>
    )
}

function Timeline({
    video, 
    videoId,
    videoTime, 
    duration, 
    setVideoTime, 
    colorPalette, 
    logData,
    showLabelInfo,
    hideLabelInfo,
    selectedLabels,
    processedScript,
    setSelectedIndex
}){
    const [position, setPosition] = useState(0);
    useEffect(() => {
    }, [videoTime]);

    const getProgressLength=()=>{
        console.log (duration)
        console.log (videoTime)
        console.log (videoTime * 850 / duration)
        if (duration == 0) return 0;
        return videoTime * 850 / duration;
    }

    const posToLabel=()=>{
        if (processedScript.length == 0) return "";
        if (videoTime <= processedScript[0].start) return processedScript[0].low_label;
        for (var i=0;i<processedScript.length;i++){
            if (processedScript[i].start < videoTime && videoTime <= processedScript[i].next_start) {
                if (processedScript[i].use) return processedScript[i].low_label;
                else return "";
            }
        }
    }

    return(
        <div className="timeline_wrapper">
            {/* <div className="timeline" onClick={handleTimelineClick} onMouseMove={handleMouseMove}/> */}
            <div className="label_timeline" style={{border: selectedLabels.length == 0 && "1px solid black"}}>
            {processedScript &&
                processedScript.map ((item, ind) => (
                <div key={ind}>
                    <LabelBox 
                        item={item} 
                        colorPalette={colorPalette} 
                        duration={duration} 
                        position={position} 
                        setVideoTime={setVideoTime} 
                        setPosition={setPosition} 
                        video={video}
                        videoTime={videoTime}
                        logData={logData}
                        showLabelInfo={showLabelInfo}
                        hideLabelInfo={hideLabelInfo}
                        setSelectedIndex={setSelectedIndex}
                    />
                </div>
                ))
            } 
            </div>
            <div className="progressbar_wrapper">
                <div className="progressbar" style={{width: `${getProgressLength()}px`}} />
                <div className="pin"><img src={pinImage} width="10px" height="50px"></img></div>
                <span className="label_tooltip">{posToLabel()}</span>   
            </div>
        </div>

    )
}

export default Timeline;

