import React, { useState, useEffect } from "react"
import { Tooltip } from "@material-ui/core";

import './Timeline.css';

function LabelBox ({item, colorPalette, duration}) {

    const calWidth = (start, end) => {
        var width = (end-start)/duration*850;
        return width;
    } 

    return (
        <div className="label_box" style={{width: calWidth(item.start, item.next_start), height: "20px", backgroundColor:colorPalette[item.low_label]}}>
        </div>
    )
}

function Timeline({video, videoTime, duration, setVideoTime, script, colorPalette}){
    const [position, setPosition] = useState(0);

    useEffect(() => {
    }, [videoTime])
  
    const handleMouseMove = event => {
        setPosition(event.clientX - event.target.offsetLeft);
    };

    const getProgressLength=()=>{
        if (duration == 0) return 0;
        return videoTime * 850 / duration;
    }

    const handleTimelineClick=()=>{
        const newTime = position * duration / 850;
        setVideoTime (newTime);
        video.seekTo (newTime);
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


    return(
        <div className="timeline_wrapper">
            <Tooltip title={posToTime (position)} placement="top">
                <div className="timeline" onClick={handleTimelineClick} onMouseMove={handleMouseMove}/>
            </Tooltip>
            <div className="label_timeline">
            {script &&
                script.map ((item, ind) => (
                <div key={ind}>
                    <LabelBox item={item} colorPalette={colorPalette} duration={duration} />
                </div>))
            } 
            </div>
            <div className="progressbar" style={{width: `${getProgressLength()}px`}} />
        </div>

    )
}

export default Timeline;

