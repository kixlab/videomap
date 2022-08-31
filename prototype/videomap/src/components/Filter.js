import React, { useState, useRef } from "react"
import { Button } from "@material-ui/core";

import './Filter.css';

const Filter = ({colorPalette}) => {
    return (
        <div className="filter_wrapper">
            <div className="category"> 
                <div className="category_label">
                    Intro
                </div>
                <div className="class">
                    <div className="group">
                        <div className="group_label">
                            Greeting
                        </div>
                        <div className="label" style={{backgroundColor: colorPalette['greeting']}}>
                            Opening
                        </div>
                    </div>
                    <div className="group">
                        <div className="group_label">
                            Overview
                        </div>
                        <div className="label" style={{backgroundColor: colorPalette['overview']}}>
                            Goal
                        </div>
                        <div className="label" style={{backgroundColor: colorPalette['overview']}}>
                            Motivation
                        </div>
                        <div className="label" style={{backgroundColor: colorPalette['overview']}}>
                            Briefing
                        </div>
                    </div>
                </div>          
            </div>
            <div className="category"> 
                <div className="category_label">
                    Procedure
                </div>
                <div className="class">          
                <div className="group">
                    <div className="group_label">
                        Step
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['step']}}>
                        Subgoal
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['step']}}>
                        Instruction
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['step']}}>
                        Tool
                    </div>
                </div>
                <div className="group">
                    <div className="group_label">
                        Supplementary
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['supplementary']}}>
                        Tip
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['supplementary']}}>
                        Warning
                    </div>
                </div>
                <div className="group">
                    <div className="group_label">
                        Explanation
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['explanation']}}>
                        Justification
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['explanation']}}>
                        Effect
                    </div>
                </div>
                <div className="group">
                    <div className="group_label">
                        Description
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['description']}}>
                        Status
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['description']}}>
                        Context
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['description']}}>
                        Tool Spec.
                    </div>
                </div>
                </div>
            </div>
            <div className="category"> 
                <div className="category_label">
                    Outro
                </div>
                <div className="class">       
                <div className="group">
                    <div className="group_label">
                        Greeting
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['greeting']}}>
                        Closing
                    </div>
                </div>
                <div className="group">
                    <div className="group_label">
                        Conclusion
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['conclusion']}}>
                        Outcome
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['conclusion']}}>
                        Reflection
                    </div>
                </div>
            </div>
            </div>
            <div className="category"> 
                <div className="category_label">
                    Misc.
                </div>
                <div className="class">
                <div className="group">
                    <div className="group_label">
                        Misc.
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['misc']}}>
                        Side Note
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['misc']}}>
                        Self-promotion
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['misc']}}>
                        Bridge
                    </div>
                    <div className="label" style={{backgroundColor: colorPalette['misc']}}>
                        Filler
                    </div>
                </div>
                </div>
            </div>
        </div>
    )
};

export default Filter;