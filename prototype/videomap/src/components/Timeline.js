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
    hideLabelInfo
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
        // console.log(event.clinetX);
        // console.log(event.target.offsetLeft);
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


        setVideoTime (newTime);
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
            {item.use 
                ? <span className="tooltiptext">{item.low_label}<br/>{posToTime(position)}</span>
                : <span className="tooltiptext">{posToTime(position)}</span>
            }
            
        </div>
    )
}

function Timeline({
    video, 
    videoTime, 
    duration, 
    setVideoTime, 
    script, 
    colorPalette, 
    logData,
    showLabelInfo,
    hideLabelInfo,
    selectedLabels,
}){
    const [position, setPosition] = useState(0);
    const [processedScript, setProcessedScript] = useState([]);

    useEffect(() => {
    }, [videoTime]);

    useEffect(() => {
        processScript ();
    }, [script, selectedLabels]);

    const processScript = () => {
        const processed = script.map (item => {
            if (selectedLabels.includes (labelInfo[item.low_label])) item['use'] = true;
            else item['use'] = false;
            return item;
        });
        // console.log (processed);
        setProcessedScript (processed);
    }

    const getProgressLength=()=>{
        if (duration == 0) return 0;
        return videoTime * 850 / duration;
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
                    />
                </div>
                ))
            } 
            </div>
            <div className="progressbar_wrapper">
                <div className="progressbar" style={{width: `${getProgressLength()}px`}} />
                <div className="pin"><img src={pinImage} width="10px" height="50px"></img></div>
            </div>
        </div>

    )
}

export default Timeline;

