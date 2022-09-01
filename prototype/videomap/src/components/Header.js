import React, { useState } from "react"
import { Box, FormControl, InputLabel, Select, MenuItem, TextField, Button } from "@material-ui/core";
import { KeyboardArrowDown, KeyboardArrowUp } from "@material-ui/icons"

import './Header.css';

function Header({videoId, setVideoId, userId, setUserId, taskId, setTaskId}){
    const [inputVideoId, setInputVideoId] = useState(videoId);
    const [inputUserId, setInputUserId] = useState(userId);
    const [inputTaskId, setInputTaskId] = useState(taskId);

    const [showInput, setShowInput] = useState (false);

    const handleInputVideoIdChange = event => {
        setInputVideoId(event.target.value);
    };

    const handleInputUserIdChange = event => {
        setInputUserId(event.target.value);
    };

    const handleInputTaskIdChange = event => {
        setInputTaskId(event.target.value);
    };

    const clickVideoIdChangeButton = () => {
        setVideoId(inputVideoId);
    };

    const clickSubmitButton = () => {
        if (inputUserId === "" || inputTaskId === "") return;
        setUserId (inputUserId);
        setTaskId (inputTaskId);
        clickShowHide();
    };

    const clickShowHide = () => {
        setShowInput (!showInput);
    }

    return(
        <div className="header_wrapper">
            {/* <h3>VIDEO MAP</h3> */}
            {showInput &&
            <div>
                <TextField 
                    InputLabelProps={{ shrink: true }}
                    id="outlined-basic" 
                    label="VIDEO ID" 
                    variant="outlined" 
                    size="small"
                    value={inputVideoId}
                    onChange={handleInputVideoIdChange}
                />
                <Button variant="contained" onClick={clickVideoIdChangeButton} style={{marginLeft: "5px"}}>Change</Button>
            
                <div className="bottom_input_wrapper">
                    <TextField 
                        InputLabelProps={{ shrink: true }}
                        id="outlined-basic" 
                        label="USER ID" 
                        variant="outlined" 
                        size="small"
                        value={inputUserId}
                        onChange={handleInputUserIdChange}
                    />
                    <TextField 
                        InputLabelProps={{ shrink: true }}
                        id="outlined-basic" 
                        label="TASK ID" 
                        variant="outlined" 
                        size="small"
                        value={inputTaskId}
                        onChange={handleInputTaskIdChange}
                        style={{marginLeft: "5px"}}
                    />
                    <Button variant="contained" onClick={clickSubmitButton} style={{marginLeft: "5px"}}>Submit</Button>
                </div>
                </div>
            }
            {showInput ? <KeyboardArrowUp onClick={clickShowHide} style={{cursor: "pointer"}}/> : <KeyboardArrowDown onClick={clickShowHide} style={{cursor: "pointer"}} />}

        </div>
    )
}

export default Header;