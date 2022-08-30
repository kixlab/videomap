import React, { useState, useEffect, useRef } from "react"
import { Tooltip, Box } from "@material-ui/core";

import './Timeline.css';
import pinImage from './../image/placeholder.png';
// import Button from 'react-bootstrap/Button';
// import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
// import Tooltip from 'react-bootstrap/Tooltip';

function LabelBox ({
    item, 
    colorPalette, 
    duration, 
    position, 
    setVideoTime, 
    setPosition,  
    video, 
    videoTime, 
    setHoverLabel, 
    logData
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
  
    const handleMouseMove = event => {
        // console.log(event.clinetX);
        // console.log(event.target.offsetLeft);
        setPosition(event.clientX - 300);
    };

    const handleTimelineClick=()=>{
        const newTime = (position * duration / 850).toFixed(2);
        // logging
        const video_timestamp = {
            from: videoTime,
            to: newTime
        }
        const meta = {
            source: "mouse", 
            location: "timeline",
        };
        logData ("jump", video_timestamp, meta);


        setVideoTime (newTime);
        video.seekTo (newTime);
    }

    const updateHoverLabel = (label) => {
        if (!label){
            setHoverLabel("");
        }
        else {
            setHoverLabel(label);
        }
    }

    return (
        <div className="label_box" onClick={handleTimelineClick} onMouseMove={handleMouseMove} onMouseOver={() => updateHoverLabel(item.low_label)} onMouseLeave={() => updateHoverLabel(false)} style={{width: calWidth(item.start, item.next_start), height: "20px", backgroundColor:colorPalette[item.low_label]}}>
            <span className="tooltiptext">{item.low_label}<br/>{posToTime(position)}</span>
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
    setHoverLabel, 
    logData
}){
    const [position, setPosition] = useState(0);
    useEffect(() => {
    }, [videoTime])

    const getProgressLength=()=>{
        if (duration == 0) return 0;
        return videoTime * 850 / duration;
    }

    return(
        <div className="timeline_wrapper">
            {/* <div className="timeline" onClick={handleTimelineClick} onMouseMove={handleMouseMove}/> */}
            <div className="label_timeline">
            {script &&
                script.map ((item, ind) => (
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
                        setHoverLabel={setHoverLabel}
                        logData={logData}
                    />
                </div>
                ))
            } 
            </div>
            <div className="progressbar_wrapper">
                <div className="progressbar" style={{width: `${getProgressLength()}px`}} />
                <div className="pin"><img src={pinImage} width="30px"></img></div>
            </div>
        </div>

    )
}

export default Timeline;

