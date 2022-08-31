import React, { useState, useRef } from "react"
import { Button } from "@material-ui/core";

import './Filter.css';

const Filter = ({colorPalette}) => {
    const onClickClass = (target) => {
        if (target.style.border === 'none'){// unselect -> select
            target.style.border = "2px solid black";
            const groups = target.nextSibling.children;
            for (var i = 0; i < groups.length; i++) {
              var group = groups[i];
              onClickGroup(group.children[0], "select");
            }
        }
        else {// select -> unselect
            target.style.border = 'none';
            const groups = target.nextSibling.children;
            for (var i = 0; i < groups.length; i++) {
              var group = groups[i];
              onClickGroup(group.children[0], "unselect");
            }
        }
    };

    const onClickGroup = (target, selected = "") => {
        if (selected == ""){
            if (target.style.border === 'none'){// unselect -> select
                updateSelected(target);
            }
            else {// select -> unselect
                updateSelected(target, "none");
            }
        }
        else {
            if (selected == "select"){// unselect -> select
                updateSelected(target, "2px solid black");
            }
            else {// select -> unselect
                updateSelected(target, "none");
            }
        }
    };

    const updateSelected = (target, selectStyle) => {
        target.style.border = selectStyle;
        var el = target.nextSibling;
        el.style.border = selectStyle;
        console.log(el.innerText);
        while (el){
            el = el.nextSibling;
            if (el){
                el.style.border = selectStyle;
                console.log(el.innerText);
            }
        }
    }

    const onClickLabel = (target) => {
        if (target.style.border === 'none'){// unselect -> select
            target.style.border = "2px solid black";
            console.log(target.innerText);
        }
        else {// select -> unselect
            target.style.border = 'none';
            console.log(target.innerText);
        }
    };
    return (
        <div className="filter_wrapper">
            <div className="category"> 
                <div className="category_label" onClick={(e)=>onClickClass(e.target)} >
                    Intro
                </div>
                <div className="class">
                    <div className="group">
                        <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                            Greeting
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['greeting']}}>
                            Opening
                        </div>
                    </div>
                    <div className="group">
                        <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                            Overview
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview']}}>
                            Goal
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview']}}>
                            Motivation
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview']}}>
                            Briefing
                        </div>
                    </div>
                </div>          
            </div>
            <div className="category"> 
                <div className="category_label" onClick={(e)=>onClickClass(e.target)}>
                    Procedure
                </div>
                <div className="class">          
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                        Step
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step']}}>
                        Subgoal
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step']}}>
                        Instruction
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step']}}>
                        Tool
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                        Supplementary
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['supplementary']}}>
                        Tip
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['supplementary']}}>
                        Warning
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                        Explanation
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['explanation']}}>
                        Justification
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['explanation']}}>
                        Effect
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                        Description
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description']}}>
                        Status
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description']}}>
                        Context
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description']}}>
                        Tool Spec.
                    </div>
                </div>
                </div>
            </div>
            <div className="category"> 
                <div className="category_label" onClick={(e)=>onClickClass(e.target)}>
                    Outro
                </div>
                <div className="class">       
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                        Greeting
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['greeting']}}>
                        Closing
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                        Conclusion
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['conclusion']}}>
                        Outcome
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['conclusion']}}>
                        Reflection
                    </div>
                </div>
            </div>
            </div>
            <div className="category"> 
                <div className="category_label" onClick={(e)=>onClickClass(e.target)}>
                    Misc.
                </div>
                <div className="class">
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)}>
                        Misc.
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc']}}>
                        Side Note
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc']}}>
                        Self-promotion
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc']}}>
                        Bridge
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc']}}>
                        Filler
                    </div>
                </div>
                </div>
            </div>
        </div>
    )
};

export default Filter;