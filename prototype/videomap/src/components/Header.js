import React, { useState } from "react"
import { TextField, Button } from "@material-ui/core";

import './Header.css';

function Header({videoId, setVideoId}){
    const [inputVideoId, setInputVideoId] = useState(videoId);

    const handleInputChange = event => {
        setInputVideoId(event.target.value);
    };

    const clickChangeButton = () => {
        setVideoId(inputVideoId);
    }

    return(
        <div className="header_wrapper">
            <h1>VIDEO MAP</h1>
            <TextField 
                InputLabelProps={{ shrink: true }}
                id="outlined-basic" 
                label="VIDEO ID" 
                variant="outlined" 
                size="small"
                value={inputVideoId}
                onChange={handleInputChange}
            />
            <Button variant="contained" onClick={clickChangeButton}>Submit</Button>
        </div>
    )
}

export default Header;