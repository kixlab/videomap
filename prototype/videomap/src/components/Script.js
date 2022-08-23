import React, { useState } from "react"
import { FormControl, FormLabel, FormControlLabel, Radio,  RadioGroup } from "@material-ui/core";

import './Script.css';


function SentenceBox ({item}) {
    const styles = {
        'opening': {background: 'rgb(249, 235, 188)'},
        'goal': {background: 'yellow'},
        'motivation': {background: 'grey'},
        'briefing': {background: 'grey'},
        'subgoal': {background: 'green '},
        'instruction': {background: 'yellow'},
        'tool': {background: 'blue'},
        'justification': {background: 'purple'},
        'effect': {background: 'white'},
        'warning': {background: 'yellow'},
        'tip': {background: 'blue'},
        'status': {background: 'lightblue'},
        'context': {background: 'lightgreen'},
        'closing': {background: 'yellow'},
        'outcome': {background: 'coral'},
        'reflection': {background: 'lightcoral'},
        'external resource': {background: 'darkorange'},
        'side note': {background: 'orange'},
        'self-promo': {background: 'yellow'},
        'bridge': {background: 'cyan'},
        'filler': {background: 'lightcyan'}
    }

    return (
        <div className="sentence_box">
            <div className="type_box">
                <span className="type" style={styles[item.Final]}>{item.Final}</span>
            </div>
            <span className="text">{item.Script}</span>
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
        setVideoTime (script[index].Start);
        video.seekTo (script[index].Start);
    };

    const handleButtonClick = (value) => {
        setTypeLevel (value);
    }

    return(
        <div className="script_wrapper">
            <FormControl>
                <FormLabel id="demo-row-radio-buttons-group-label">LEVEL</FormLabel>
                <RadioGroup
                    row
                    aria-labelledby="demo-row-radio-buttons-group-label"
                    name="row-radio-buttons-group"
                >
                    <FormControlLabel value="high" control={<Radio />} label="HIGH" />
                    <FormControlLabel value="low" control={<Radio />} label="LOW" />
                </RadioGroup>
            </FormControl>
            <div className="script_block">
                {script &&
                    script.map ((item, ind) => (
                    <div key={ind} className={selectedIndex == ind ? "selected" : "default"} onClick={() => handleSentenceClick(ind)}>
                        <SentenceBox item={item} />
                    </div>))
                }
            </div>
        </div>
    )
}

export default Script;