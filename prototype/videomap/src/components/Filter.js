import React, { useState, useEffect, useRef } from "react"
import { Tooltip, Box } from "@material-ui/core";

import './Filter.css';
import { definition } from "../definition";
import { BorderStyle } from "@material-ui/icons";
import { labelMapping } from "../labelMapping";

const Filter = ({colorPalette, selectedLabels, setSelectedLabels, logData, videoTime}) => {
    const [selectStatus, setSelectStatus] = useState({'greeting_intro':1, 'overview':3, 'step': 3, 'supplementary':2, 'explanation':2, 'description':3, 'greeting_outro': 1, 'conclusion':2, 'misc':4});
    const fullSelectStatus = {'greeting_intro':1, 'overview':3, 'step': 3, 'supplementary':2, 'explanation':2, 'description':3, 'greeting_outro': 1, 'conclusion':2, 'misc':4};


    useEffect(()=>{
        for (var key in selectStatus){
            if(selectStatus[key] == fullSelectStatus[key]){
                const target = document.getElementById(key);
                onSelectGroup(target);
                target.classList.add("selected");
            }
            else {
                const target = document.getElementById(key);
                onUnselectGroup(target);
                target.classList.remove("selected");
            }
        }
    }, [selectStatus]);

    const onClickGroup = (target, selected = "") => {
        if (selected == ""){
            var select;
            if (target.classList.contains("selected")){ //unselect
                onUpdateGroup(target, "unselect");
                target.classList.toggle("selected");
                select = "unselect";
            }
            else {//select
                onUpdateGroup(target, "select");
                target.classList.toggle("selected");
                select = "select";
            }
            // logging
            const meta = {
                level: "high",
                label: target.id,
                select: select
            };
            logData ("filter", videoTime, meta);
        }
        else {
            onUpdateGroup(target, selected)
        }
    };

    const onUpdateGroup = (target, selected) => {
        var label_list = [];
        var el = target.nextSibling;
        onClickLabel (el, selected);
        label_list.push(el.children[0].id);
        while (el){
            el = el.nextSibling;
            if (el){
                onClickLabel (el, selected);
                label_list.push(el.children[0].id);
            }
        }
        if (selected == "unselect") {
            onUnselectGroup(target);
            updateSelectedLabelList(label_list, "remove")
        }
        else {
            onSelectGroup(target);
            updateSelectedLabelList(label_list, "add")
        }
    }

    const onSelectGroup = (target) => {
        target.style.backgroundColor = "rgb(82, 82, 82)";
        target.style.color = colorPalette[target.innerText];
        target.style.border = "3px solid rgb(82, 82, 82)";

    }

    const onUnselectGroup = (target) => {
        target.style.backgroundColor = "white";
        target.style.color = "black";
    }

    const onClickLabel = (target, selected="") => {
        var select;
        if (selected == ""){
            if (target.classList.contains("selected")){ //unselect
                target.style.border = "3px solid " + colorPalette[target.children[0].id];
                target.style.backgroundColor = "white";
                target.classList.toggle("selected");
                updateSelectedLabel(target.children[0].id, "remove");
                const group_label = target.parentElement.children[0].id;
                updateGroupCount (group_label, -1);
                select = "unselect";
            }
            else { //select
                if (target.children[0]){
                    target.style.backgroundColor = colorPalette[target.children[0].id];
                    target.classList.toggle("selected");
                    updateSelectedLabel(target.children[0].id, "add");
                    const group_label = target.parentElement.children[0].id;
                    updateGroupCount (group_label, 1);
                    select = "select";
                }
            }

            // logging (direct low label filter)
            const meta = {
                level: "low",
                label: labelMapping[target.children[0].id],
                select: select
            };
            logData ("filter", videoTime, meta);

        }
        else {
            if (selected == "select"){ //select
                target.style.backgroundColor = colorPalette[target.children[0].id];
                target.classList.add("selected");
                updateSelectedLabel(target.children[0].id, "add");
                // const group_label = target.parentElement.children[0].id;
                // updateGroupCount (group_label, 1);
            }
            else { //unselect
                target.style.border = "3px solid " + colorPalette[target.children[0].id];
                target.style.backgroundColor = "white";
                target.classList.remove("selected");
                updateSelectedLabel(target.children[0].id, "remove");
                // const group_label = target.parentElement.children[0].id;
                // updateGroupCount (group_label, -1);
            }

        }
    };

    const updateGroupCount = (label, add, force = false) => {
        if (force){ 
            const currGroupCountState = {...selectStatus}
            currGroupCountState[label] =  add;
            setSelectStatus(currGroupCountState);

        }
        else {
            const currGroupCountState = {...selectStatus}
            currGroupCountState[label] = selectStatus[label] + add;
            setSelectStatus(currGroupCountState);
        }
    }

    const updateSelectedLabelList = (label_list, selectStyle) => {
        const example = label_list[0];
        const group_label = document.getElementById(example).parentElement.parentElement.children[0].id;

        if (selectStyle == "add") {
            // https://www.samanthaming.com/tidbits/87-5-ways-to-append-item-to-array/
            const label_set = new Set(selectedLabels);
            const add_label_set = new Set(label_list)
            const labels = new Set([...label_set, ...add_label_set]);
            const final_labels = [...labels]
            // const labels = selectedLabels.concat(label_list);
            setSelectedLabels(final_labels);
            updateGroupCount(group_label, label_list.length, true);
        }
        else {
            const label_set = new Set(selectedLabels);
            const remove_label_set = new Set(label_list);
            const labels = new Set([...label_set].filter(x => !remove_label_set.has(x)));
            const final_labels = [...labels];
            setSelectedLabels(final_labels);
            updateGroupCount(group_label, 0, true);
        }
    }

    const updateSelectedLabel = (label, selectStyle) => {
        if (selectStyle == "add") {
            const labels = [...selectedLabels, label];
            // console.log (labels);
            setSelectedLabels(labels);
        }
        else {
            const labels = selectedLabels.filter(item => item!=label);
            // console.log (labels);
            setSelectedLabels(labels);
        }
    }

    const onClickSelectAll = () => {
        const groups = document.getElementsByClassName("group_label");
        for (var i = 0; i < groups.length; i++) {
          var group = groups[i];
          onClickGroup(group, "select");
          setSelectStatus({'greeting_intro':1, 'overview':3, 'step': 3, 'supplementary':2, 'explanation':2, 'description':3, 'greeting_outro': 1, 'conclusion':2, 'misc':4});
        }
        setSelectedLabels(["opening", "goal", "motivation", "briefing", "subgoal", "instruction", "tool", "justification", "effect", "tip", "warning", "status", "context", "tool-spec", "closing", "outcome", "reflection", "side-note", "self-promo", "bridge", "filler"]);

        // logging
        const meta = {
            level: "all",
            select: "select"
        };
        logData ("filter", videoTime, meta);
    }

    const onClickUnselectAll = () => {
        const groups = document.getElementsByClassName("group_label");
        for (var i = 0; i < groups.length; i++) {
          var group = groups[i];
          onClickGroup(group, "unselect");
          setSelectStatus({'greeting_intro':0, 'overview':0, 'step': 0, 'supplementary':0, 'explanation':0, 'description':0, 'greeting_outro': 0, 'conclusion':0, 'misc':0});
        }
        
        setSelectedLabels([]);

        // logging
        const meta = {
            level: "all",
            select: "unselect"
        }
        logData ("filter", videoTime, meta);

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
                        <div className="group_label selected" id="greeting_intro" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['greeting']}}>
                            Greeting
                        </div>
                        <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['greeting'], borderColor: colorPalette['greeting']}}>
                            Opening
                            <span className="tooltiptext" id="opening">{definition['opening']}</span>
                        </div>
                    </div>
                    <div className="group">
                        <div className="group_label selected" id="overview"  onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['overview']}}>
                            Overview
                        </div>
                        <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview'], borderColor: colorPalette['overview']}}>
                            Goal
                            <span className="tooltiptext" id="goal">{definition['goal']}</span>
                        </div>
                        <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview'], borderColor: colorPalette['overview']}}>
                            Motivation
                            <span className="tooltiptext" id="motivation">{definition['motivation']}</span>
                        </div>
                        <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['overview'], borderColor: colorPalette['overview']}}>
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
                    <div className="group_label selected" id="step"  onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['step']}}>
                        Step
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step'], borderColor: colorPalette['step']}}>
                        Subgoal
                            <span className="tooltiptext" id="subgoal">{definition['subgoal']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step'], borderColor: colorPalette['step']}}>
                        Instruction
                            <span className="tooltiptext" id="instruction">{definition['instruction']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['step'], borderColor: colorPalette['step']}}>
                        Tool
                            <span className="tooltiptext" id="tool">{definition['tool']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label selected" id="supplementary"  onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['supplementary']}}>
                        Supplementary
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['supplementary'], borderColor: colorPalette['supplementary']}}>
                        Tip
                            <span className="tooltiptext" id="tip">{definition['tip']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['supplementary'], borderColor: colorPalette['supplementary']}}>
                        Warning
                            <span className="tooltiptext" id="warning">{definition['warning']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label selected" id="explanation"  onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['explanation']}}>
                        Explanation
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['explanation'], borderColor: colorPalette['explanation']}}>
                        Justification
                            <span className="tooltiptext" id="justification">{definition['justification']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['explanation'], borderColor: colorPalette['explanation']}}>
                        Effect
                            <span className="tooltiptext" id="effect">{definition['effect']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label selected" id="description"  onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['description']}}>
                        Description
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description'], borderColor: colorPalette['description']}}>
                        Status
                            <span className="tooltiptext" id="status">{definition['status']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description'], borderColor: colorPalette['description']}}>
                        Context
                            <span className="tooltiptext" id="context">{definition['context']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['description'], borderColor: colorPalette['description']}}>
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
                    <div className="group_label selected" id="greeting_outro"  onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['greeting']}}>
                        Greeting
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['greeting'], borderColor: colorPalette['greeting']}}>
                        Closing
                            <span className="tooltiptext" id="closing">{definition['closing']}</span>
                    </div>
                </div>
                <div className="group">
                    <div className="group_label" id="conclusion"  onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['conclusion']}}>
                        Conclusion
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['conclusion'], borderColor: colorPalette['conclusion']}}>
                        Outcome
                            <span className="tooltiptext" id="outcome">{definition['outcome']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['conclusion'], borderColor: colorPalette['conclusion']}}>
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
                    <div className="group_label selected" id="misc" onClick={(e)=>onClickGroup(e.target)} style={{color: colorPalette['misc']}}>
                        Misc.
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc'], borderColor: colorPalette['misc']}}>
                        Side Note
                            <span className="tooltiptext" id="side-note">{definition['side note']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc'], borderColor: colorPalette['misc']}}>
                        Self-promotion
                            <span className="tooltiptext" id="self-promo">{definition['self-promo']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc'], borderColor: colorPalette['misc']}}>
                        Bridge
                            <span className="tooltiptext" id="bridge">{definition['bridge']}</span>
                    </div>
                    <div className="label selected" onClick={(e)=>onClickLabel(e.target)} style={{backgroundColor: colorPalette['misc'], borderColor: colorPalette['misc']}}>
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