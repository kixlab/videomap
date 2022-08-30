import React, { useState, useEffect } from "react"
import { Tooltip } from "@material-ui/core";

import './Timeline.css';
import pinImage from './../image/placeholder.png';

function LabelBox ({item, colorPalette, duration}) {

    const calWidth = (start, end) => {
        var width = (end-start)/duration*850;
        return width;
    } 

    return (
        <Tooltip title="hello" placement="right">
        <div className="label_box" style={{width: calWidth(item.start, item.next_start), height: "20px", backgroundColor:colorPalette[item.low_label]}}>
            {/* <div>{item.low_label}</div> */}
        </div>
        </Tooltip>
    )
}

function Timeline({video, videoTime, duration, setVideoTime, script, colorPalette}){
    const [position, setPosition] = useState(0);

    useEffect(() => {
    }, [videoTime])
  
    const handleMouseMove = event => {
        setPosition(event.clientX - event.target.offsetLeft - 300);
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
        {/* <Tooltip title="hello" placement="bottom"> */}
                <div className="timeline" onClick={handleTimelineClick} onMouseMove={handleMouseMove}/>
                {/* </Tooltip> */}
            <div className="label_timeline">
            {script &&
                script.map ((item, ind) => (

           
                <div key={ind}>
                    <LabelBox item={item} colorPalette={colorPalette} duration={duration} />
                </div>
                ))
            } 
            </div>
            <div className="progressbar_wrapper">
                <div className="progressbar" style={{width: `${getProgressLength()}px`}} />
                <div className="pin"><img src={pinImage} width="50px"></img></div>
            </div>
        </div>

    )
}

export default Timeline;

