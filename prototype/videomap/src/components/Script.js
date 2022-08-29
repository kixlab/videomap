import React, { useState } from "react"
import { FormControl, FormLabel, FormControlLabel, Radio,  RadioGroup } from "@material-ui/core";

import './Script.css';


function SentenceBox ({item, typeLevel}) {
    const styles = {
        // high type
        'greeting': {background: 'yellow'},
        'overview': {background: 'green '},
        'step': {background: 'purple'},
        'supplementary': {background: 'white'},
        'explanation': {background: 'lightblue'},
        'description': {background: 'yellow'},
        'conclusion': {background: 'blue'},
        'misc.': {background: 'lightcyan'},
        // low type
        //greeting
        'opening': {background: '#DAF283'},
        //overview
        'goal': {background: '#F6BD60'},
        'motivation': {background: '#F6BD60'},
        'briefing': {background: '#F6BD60'},
        //step
        'subgoal': {background: '#F5A7A6 '},
        'instruction': {background: '#F5A7A6'},
        'tool': {background: '#F5A7A6'},
        'tool (multiple)': {background: '#F5A7A6'},
        'tool (optional)': {background: '#F5A7A6'},
        //explanation
        'justification': {background: '#FFF5AB'},
        'effect': {background: '#FFF5AB'},
        //supplementary
        'warning': {background: '#C7B4C4'},
        'tip': {background: '#C7B4C4'},
        //description
        'status': {background: '#A8D0C6'},
        'context': {background: '#A8D0C6'},
        'tool spec.': {background: '#A8D0C6'},
        //greeting-outro
        'closing': {background: '#DAF283'},
        //conclusion
        'outcome': {background: '#DCC8E6'},
        'reflection': {background: '#DCC8E6'},
        //misc
        'side note': {background: 'lightgray'},
        'self-promo': {background: 'lightgray'},
        'bridge': {background: 'lightgray'},
        'filler': {background: 'lightgray'}
    }

    const transTime = (timestamp) => {
        var seconds = parseFloat(timestamp)
        var minute = Math.floor(seconds / 60);
        var second = Math.floor(seconds - minute * 60);
        // if (minute < 10){
        //     minute = "0"+minute
        // }
        if (second < 10){
            second = "0"+second
        }
        return "(" + minute + ":" + second + ")"
    }

    return (
        <div className="sentence_box">
            <div className="type_box">
                <div className="type" style={typeLevel == 'low' ? styles[item.low_label] : styles[item.high_label]}>
                    {typeLevel == 'low' ? item.low_label : item.high_label}
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
    setVideoTime
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
                        <SentenceBox item={item} typeLevel = {typeLevel} />
                    </div>))
                }
            </div>
        </div>
    )
}

export default Script;