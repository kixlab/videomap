import React, { useState, useRef } from "react"
import { Button } from "@material-ui/core";

import './Filter.css';

const Filter = ({colorPalette}) => {
    return (
        <div className="filter_wrapper">
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['greeting']}}>
                    Greeting
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['greeting']}}>
                    Opening
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label">
                    Overview
                </div>
                <div className="filter_label">
                    Goal
                </div>
                <div className="filter_label">
                    Motivation
                </div>
                <div className="filter_label">
                    Briefing
                </div>
            </div>
        </div>
    )
};

export default Filter;