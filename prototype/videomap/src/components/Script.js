import React, { useEffect } from "react"

import './Script.css';


function SentenceBox ({item, colorPalette, showLabelInfo, hideLabelInfo}) {

    const transTime = (timestamp) => {
        var seconds = parseFloat(timestamp)
        var minute = Math.floor(seconds / 60);
        var second = Math.floor(seconds - minute * 60);
        if (second < 10){
            second = "0"+second
        }
        return "(" + minute + ":" + second + ")"
    }

    return (
        <div className="sentence_box">
            <div className="type_box">
                <div className="type" style={{backgroundColor: colorPalette[item.low_label] }} onMouseEnter={() => showLabelInfo(item.low_label)} onMouseLeave={() => hideLabelInfo(item.low_label)}>
                   {item.low_label}
                   {/* <span className="tooltiptext">{item.low_label}<br/>{"definition"}</span> */}
                </div>
            </div>
            <div className="time">{transTime(item.start)}</div>
            <div className="text">{item.script}</div>
        </div>
    )
}

function Script({
    script, 
    selectedIndex, 
    setSelectedIndex, 
    video, 
    videoTime, 
    setVideoTime,
    colorPalette,
    logData,
    filteredScript,
    showLabelInfo,
    hideLabelInfo
}){

    useEffect (() => {
    }, [filteredScript])

    const handleSentenceClick = (index) => {
        // logging
        const currLine = script[index];
        const newTime = script[index].start;
        const video_timestamp = {
            from: videoTime,
            to: newTime
        }
        const meta = {
            source: "mouse", 
            location: "script",
            low_label: currLine.low_label,
            high_label: currLine.high_label
        };
        logData ("jump", video_timestamp, meta);

        setSelectedIndex (index);
        // setVideoTime (newTime);
        video.seekTo (newTime);
    };

    return(
        <div className="script_window">
            {filteredScript.length == 0? <div className="warning_message">Please select at least one label.</div>:
            <div className="script_block">
                {filteredScript &&
                    filteredScript.map ((item, ind) => (
                    <div key={ind} id={ind} className={selectedIndex == item.index ? "selected " + item.index : "default " + item.index} onClick={() => handleSentenceClick(item.index)}>
                        <SentenceBox item={item} colorPalette={colorPalette} showLabelInfo={showLabelInfo} hideLabelInfo={hideLabelInfo}/>
                    </div>))
                }
            </div>
            }
        </div>
    )
}

export default Script;