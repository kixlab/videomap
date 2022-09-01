import React, { useState, useRef } from "react"
import { Button } from "@material-ui/core";

import './Filter.css';

const Filter = ({colorPalette, selectedLabels, setSelectedLabels}) => {
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
                updateSelected(target, "2px solid black");
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
        var label_list = [];
        label_list.push(el.innerText);
        while (el){
            el = el.nextSibling;
            if (el){
                el.style.border = selectStyle;
                label_list.push(el.innerText);
            }
        }
        if (selectStyle == "none") {
            updateSelectedLabelList(label_list, "remove")
        }
        else {
            updateSelectedLabelList(label_list, "add")
        }
    }

    const onClickLabel = (target) => {
        if (target.style.border === 'none'){// unselect -> select
            target.style.border = "2px solid black";
            updateSelectedLabels(target.innerText, "add")
        }
        else {// select -> unselect
            target.style.border = 'none';
            updateSelectedLabels(target.innerText, "remove")
        }
    };

    const updateSelectedLabelList = (label_list, selectStyle) => {
        if (selectStyle == "add") {
            // https://www.samanthaming.com/tidbits/87-5-ways-to-append-item-to-array/
            const labels = selectedLabels.concat(label_list);
            setSelectedLabels(labels);
        }
        else {
            const label_set = new Set(selectedLabels);
            const remove_label_set = new Set(label_list);
            const labels = new Set([...label_set].filter(x => !remove_label_set.has(x)));
            const final_labels = [...labels];
            setSelectedLabels(final_labels);
        }
    }

    const updateSelectedLabels = (label, selectStyle) => {
        if (selectStyle == "add") {
            const labels = [...selectedLabels, label];
            setSelectedLabels(labels);
        }
        else {
            const labels = selectedLabels.filter(item => item!=label);
            setSelectedLabels(labels);
        }
    }

    const onClickSelectAll = () => {
        const groups = document.getElementsByClassName("group_label");
        for (var i = 0; i < groups.length; i++) {
          var group = groups[i];
          onClickGroup(group, "select");
        }
        setSelectedLabels(["Opening", "Goal", "Motivation", "Briefing", "Subgoal", "Instruction", "Tool", "Justification", "Effect", "Tip", "Warning", "Status", "Context", "Tool spec.", "Closing", "Outcome", "Reflection", "Side note", "Self-promo", "Bridge", "Filler"]);
    }

    const onClickUnselectAll = () => {
        const groups = document.getElementsByClassName("group_label");
        for (var i = 0; i < groups.length; i++) {
          var group = groups[i];
          onClickGroup(group, "unselect");
        }
        setSelectedLabels([]);

    }

    const onMouseEnter = (e) => {
        e.target.style.backgroundColor = "black";
        e.target.style.color = "white";
    }

    const onMouseLeave = (e) => {
        e.target.style.backgroundColor = "white";
        e.target.style.color = "black";
    }

    return (
        <div className="filter_wrapper">
            <div className="select">
                <div className="selectBtn" onClick={()=>onClickSelectAll()} onMouseEnter={(e)=>onMouseEnter(e)} onMouseLeave={(e)=>onMouseLeave(e)}>Select All</div>
                <div className="selectBtn" onClick={()=>onClickUnselectAll()} onMouseEnter={(e)=>onMouseEnter(e)} onMouseLeave={(e)=>onMouseLeave(e)}>Unselect All</div>
            </div>
            <div className="label_wrapper">
            <div className="category"> 
                <div className="category_label" >
                    Intro
                </div>
                <div className="class">
                    <div className="group">
                        <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['greeting']}}>
                            Greeting
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['greeting']}}>
                            Opening
                        </div>
                    </div>
                    <div className="group">
                        <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['overview']}}>
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
                <div className="category_label">
                    Procedure
                </div>
                <div className="class">          
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['step']}}>
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
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['supplementary']}}>
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
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['explanation']}}>
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
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['description']}}>
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
                <div className="category_label">
                    Outro
                </div>
                <div className="class">       
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['greeting']}}>
                        Greeting
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['greeting']}}>
                        Closing
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['conclusion']}}>
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
                <div className="category_label">
                    Misc.
                </div>
                <div className="class">
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['misc']}}>
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
        </div>
    )
};

export default Filter;