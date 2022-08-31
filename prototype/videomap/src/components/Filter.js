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
                <div className="filter_high_label" style={{backgroundColor: colorPalette['overview']}}>
                    Overview
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['overview']}}>
                    Goal
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['overview']}}>
                    Motivation
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['overview']}}>
                    Briefing
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['step']}}>
                    Step
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['step']}}>
                    Subgoal
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['step']}}>
                    Instruction
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['step']}}>
                    Tool
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['supplementary']}}>
                    Supplementary
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['supplementary']}}>
                    Tip
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['supplementary']}}>
                    Warning
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['explanation']}}>
                    Explanation
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['explanation']}}>
                    Justification
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['explanation']}}>
                    Effect
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['description']}}>
                    Description
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['description']}}>
                    Status
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['description']}}>
                    Context
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['description']}}>
                    Tool Specification
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['greeting']}}>
                    Greeting
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['greeting']}}>
                    Closing
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['conclusion']}}>
                    Conclusion
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['conclusion']}}>
                    Outcome
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['conclusion']}}>
                    Reflection
                </div>
            </div>
            <div className="filter_group">
                <div className="filter_high_label" style={{backgroundColor: colorPalette['misc']}}>
                    Misc.
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['misc']}}>
                    Side Note
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['misc']}}>
                    Self-promotion
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['misc']}}>
                    Bridge
                </div>
                <div className="filter_label" style={{backgroundColor: colorPalette['misc']}}>
                    Filler
                </div>
            </div>
        </div>
    )
};

export default Filter;