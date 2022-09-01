import React, { useState, useEffect, useRef } from "react"
import { Tooltip, Box } from "@material-ui/core";

import './Filter.css';
import { definition } from "../definition";

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
        label_list.push(el.children[0].id);
        while (el){
            el = el.nextSibling;
            if (el){
                el.style.border = selectStyle;
                label_list.push(el.children[0].id);
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
        console.log(target)
        console.log (target.style.border)
        if (target.style.border === 'none'){// unselect -> select
            target.style.border = "2px solid black";
            updateSelectedLabels(target.children[0].id, "add")
        }
        else {// select -> unselect
            target.style.border = 'none';
            updateSelectedLabels(target.children[0].id, "remove")
        }
    };

    const updateSelectedLabelList = (label_list, selectStyle) => {
        if (selectStyle == "add") {
            // https://www.samanthaming.com/tidbits/87-5-ways-to-append-item-to-array/
            const label_set = new Set(selectedLabels);
            const add_label_set = new Set(label_list)
            const labels = new Set([...label_set, ...add_label_set]);
            const final_labels = [...labels]
            // const labels = selectedLabels.concat(label_list);
            setSelectedLabels(final_labels);
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
            console.log (labels);
            setSelectedLabels(labels);
        }
        else {
            const labels = selectedLabels.filter(item => item!=label);
            console.log (labels);
            setSelectedLabels(labels);
        }
    }

    const onClickSelectAll = () => {
        const groups = document.getElementsByClassName("group_label");
        for (var i = 0; i < groups.length; i++) {
          var group = groups[i];
          onClickGroup(group, "select");
        }
        setSelectedLabels(["opening", "goal", "motivation", "briefing", "subgoal", "instruction", "tool", "justification", "effect", "tip", "warning", "status", "context", "tool-spec", "closing", "outcome", "reflection", "side-note", "self-promo", "bridge", "filler"]);
    }

    const onClickUnselectAll = () => {
        const groups = document.getElementsByClassName("group_label");
        for (var i = 0; i < groups.length; i++) {
          var group = groups[i];
          onClickGroup(group, "unselect");
        }
        setSelectedLabels([]);

    }

    const onSelect = (e) => {
        e.target.style.backgroundColor = "black";
        e.target.style.color = "white";
    }

    const onUnselect = (e) => {
        e.target.style.backgroundColor = "white";
        e.target.style.color = "black";
    }

    return (
        <div className="filter_wrapper">
            <div className="select">
                <div className="selectBtn" onClick={()=>onClickSelectAll()} onMouseEnter={(e)=>onSelect(e)} onMouseLeave={(e)=>onUnselect(e)}>Select All</div>
                <div className="selectBtn" onClick={()=>onClickUnselectAll()} onMouseEnter={(e)=>onSelect(e)} onMouseLeave={(e)=>onUnselect(e)}>Unselect All</div>
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
                            <span className="tooltiptext" id="opening">{definition['opening']}</span>
                        </div>
                    </div>
                    <div className="group">
                        <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['overview']}}>
                            Overview
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview']}}>
                            Goal
                            <span className="tooltiptext" id="goal">{definition['goal']}</span>
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview']}}>
                            Motivation
                            <span className="tooltiptext" id="motivation">{definition['motivation']}</span>
                        </div>
                        <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview']}}>
                            Briefing
                            <span className="tooltiptext" id="briefing">{definition['briefing']}</span>
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
                            <span className="tooltiptext" id="subgoal">{definition['subgoal']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step']}}>
                        Instruction
                            <span className="tooltiptext" id="instruction">{definition['instruction']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step']}}>
                        Tool
                            <span className="tooltiptext" id="tool">{definition['tool']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['supplementary']}}>
                        Supplementary
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['supplementary']}}>
                        Tip
                            <span className="tooltiptext" id="tip">{definition['tip']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['supplementary']}}>
                        Warning
                            <span className="tooltiptext" id="warning">{definition['warning']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['explanation']}}>
                        Explanation
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['explanation']}}>
                        Justification
                            <span className="tooltiptext" id="justification">{definition['justification']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['explanation']}}>
                        Effect
                            <span className="tooltiptext" id="effect">{definition['effect']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['description']}}>
                        Description
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description']}}>
                        Status
                            <span className="tooltiptext" id="status">{definition['status']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description']}}>
                        Context
                            <span className="tooltiptext" id="context">{definition['context']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description']}}>
                        Tool Spec.
                            <span className="tooltiptext" id="tool-spec">{definition['tool spec.']}</span>
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
                            <span className="tooltiptext" id="closing">{definition['closing']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['conclusion']}}>
                        Conclusion
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['conclusion']}}>
                        Outcome
                            <span className="tooltiptext" id="outcome">{definition['outcome']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['conclusion']}}>
                        Reflection
                            <span className="tooltiptext" id="reflection">{definition['reflection']}</span>
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
                            <span className="tooltiptext" id="side-note">{definition['side note']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc']}}>
                        Self-promotion
                            <span className="tooltiptext" id="self-promo">{definition['self-promo']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc']}}>
                        Bridge
                            <span className="tooltiptext" id="bridge">{definition['bridge']}</span>
                    </div>
                    <div className="label" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc']}}>
                        Filler
                            <span className="tooltiptext" id="filler">{definition['filler']}</span>
                    </div>
                </div>
                </div>
            </div>
            </div>
        </div>
    )
};

export default Filter;