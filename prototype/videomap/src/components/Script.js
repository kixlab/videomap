import React, { useState } from "react"
import { FormControl, FormLabel, FormControlLabel, Radio,  RadioGroup } from "@material-ui/core";

import './Script.css';


function SentenceBox ({item, typeLevel, colorPalette}) {

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
                <div className="type" style={{backgroundColor: colorPalette[item.low_label] }}>
                   {item.low_label}
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
    colorPalette
}){
    const [typeLevel, setTypeLevel] = useState ('low');

    const handleSentenceClick = (index) => {
        setSelectedIndex (index);
        setVideoTime (script[index].start);
        video.seekTo (script[index].start);
    };

    const handleRadioClick = (event) => {
        setTypeLevel(event.target.value);
      };

    return(
        <div className="script_window">
            {/* <FormControl>
                <FormLabel id="demo-row-radio-buttons-group-label">LEVEL</FormLabel>
                <RadioGroup
                    row
                    aria-labelledby="demo-row-radio-buttons-group-label"
                    name="row-radio-buttons-group"
                    defaultValue={"low"}
                    onChange={handleRadioClick}
                >
                    <FormControlLabel value="high" control={<Radio />} label="HIGH" />
                    <FormControlLabel value="low" control={<Radio />} label="LOW" />
                </RadioGroup>
            </FormControl> */}
            <div className="script_block">
                {script &&
                    script.map ((item, ind) => (
                    <div key={ind} className={selectedIndex == ind ? "selected" : "default"} onClick={() => handleSentenceClick(ind)}>
                        <SentenceBox item={item} typeLevel = {typeLevel} colorPalette={colorPalette}/>
                    </div>))
                }
            </div>
        </div>
    )
}

export default Script;