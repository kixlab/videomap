import React, { useState, useEffect, useCallback } from 'react'
import db from "./service/firebase";
import { ref, update } from "firebase/database";
import YouTube from 'react-youtube';
import './App.css';
import { colorPalette } from "./colors";
import { category } from "./category";
import { labelInfo } from "./labelInfo";

// components
import Header from './components/Header';
import Script from './components/Script';
import Timeline from './components/Timeline';
import Filter from './components/Filter';

function App() {
  const [video, setVideo] = useState (null);
  const [started, setStarted] = useState(false);
  const [isPlaying, setIsPlaying] = useState (false);

  const [videoId, setVideoId] = useState ('6CJryveLzvI');
  const [videoTime, setVideoTime] = useState (0);
  const [duration, setDuration] = useState (0);

  const [scriptLoaded, setScriptLoaded] = useState (false);
  const [script, setScript] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState (-1);

  // filter
  const [selectedLabels, setSelectedLabels] = useState (["opening", "goal", "motivation", "briefing", "subgoal", "instruction", "tool", "justification", "effect", "tip", "warning", "status", "context", "tool-spec", "closing", "outcome", "reflection", "side-note", "self-promo", "bridge", "filler"]);
  const [filteredScript, setFilteredScript] = useState ([]);

  // for log
  // Task Id
  // 0 for search, 1 for skim and summary, 2 for following
  const [userId, setUserId] = useState("");
  const [taskId, setTaskId] = useState("");
  const [initialTimeInfo, setInitialTimeInfo] = useState (null);
  const [logIndex, setLogIndex] = useState (0);

  // database
  const logData=(action, video_timestamp, meta, firstLog=false)=>{
    if (videoId === "" || userId === "" || taskId === "") return;

    const save_path = '/Log' + '/' + userId + '/' + videoId + '/' + taskId;
    const user_timestamp = firstLog ? 0 : (new Date().getTime() / 1000 - initialTimeInfo).toFixed(3);
    const updates = {};
    updates[save_path + '/' + logIndex] = {
      action: action,
      video_timestamp: video_timestamp,
      user_timestamp: user_timestamp,
      meta: meta
    }
    const nextLogIndex = logIndex + 1;
    setLogIndex (nextLogIndex);

    return update (ref (db), updates);
  }
  
  const getScript=()=>{
    fetch(process.env.PUBLIC_URL + `/data/${videoId}.json`)
      .then(function (response){
        return response.json();
      })
      .then(function (jsonFile) {
        setScript (jsonFile);
        setSelectedIndex (0);
        setScriptLoaded (true);
        // filter
        setFilteredScript (jsonFile);
      });
  };

  useEffect(()=>{
    getScript();
  }, [videoId]);

  // filter script
  const filterScript = () => {
    const filtered = script.filter (item => selectedLabels.includes (labelInfo[item.low_label]));
    const newIndex = filtered.length > 0 ? filtered[0].index : -1;
    setFilteredScript (filtered);
    setSelectedIndex (newIndex);
}

  useEffect(() => {
    if (script.length > 0) {
        filterScript();
    }
}, [selectedLabels])

  const logKeyPress = (keyCode, scriptIndex = -1) => {
    var video_timestamp = {};
    var meta = {};
    if (keyCode === "up" || keyCode === "down") {
      const currLine = script[scriptIndex]
      video_timestamp = {from: videoTime, to: currLine.start};
      meta = {
        source: "keyboard",
        key: keyCode,
        low_label: currLine.low_label,
        high_label: currLine.high_label
      };
    } else {
      video_timestamp = keyCode === "left" 
                      ? {from: videoTime, to: (parseFloat(videoTime) - 5).toFixed(3)}
                      : {from: videoTime, to: (parseFloat(videoTime) + 5).toFixed(3)};
      meta = {
        source: "keyboard",
        key: keyCode
      };
    }

    logData ("jump", video_timestamp, meta);
  }

  const getNextIndex = (script, currentIndex) => {
    for (var i = 0; i < script.length; i++) {
      if (script[i].index === currentIndex) {
        return script[i+1].index;
      }
    }
  };

  const getPreviousIndex = (script, currentIndex) => {
    for (var i = 0; i < script.length; i++) {
      if (script[i].index === currentIndex) {
        return script[i-1].index;
      }
    }
  }

  const onKeyPress = (e) => {
    const keyCode = e.keyCode;
    let ind, vt;

    // up arrow
    if (keyCode == 38) {
      if (selectedIndex > filteredScript[0].index) {
        ind = getPreviousIndex (filteredScript, selectedIndex);
        // logging
        logKeyPress ("up", ind);
        handleIndexChange (ind);
      } 

    // down arrow
    } else if (keyCode == 40) { 
      if (selectedIndex < filteredScript[filteredScript.length-1].index) {
        ind = getNextIndex (filteredScript, selectedIndex);
        // logging
        logKeyPress ("down", ind);
        handleIndexChange (ind);
      }
    // left arrow
    } else if (keyCode == 37) {
      // logging
      logKeyPress ("left");
      vt = (parseFloat(videoTime) - 5).toFixed(3);
      setVideoTime (vt);
      video.seekTo (vt);

    // right arrow
    } else if (keyCode == 39) {
      // logging
      logKeyPress ("right", ind);
      vt = (parseFloat(videoTime) + 5).toFixed(3);
      setVideoTime (vt);
      video.seekTo (vt);
    // space 
    } else if (keyCode == 32) { 
      if(e.target == document.body) {
        e.preventDefault();
      }
      const currentStatus = video.getPlayerState();
      if (currentStatus == 0 || currentStatus == 2 || currentStatus == 5) video.playVideo();
      else if (currentStatus == 1) video.pauseVideo();
    };
  };

  const handleIndexChange = (index) => {
    setSelectedIndex (index);
    setVideoTime (script[index].start);
    video.seekTo (script[index].start);
  };

  useEffect(() => { //TODO: update?
    if (video && scriptLoaded) {
      document.addEventListener('keydown', onKeyPress);
      return function cleanup() {
        document.removeEventListener('keydown', onKeyPress);
      }
    };
  }, [video, videoTime, scriptLoaded, selectedIndex]);

  // TODO: fix bug
  // useEffect(() => {
  //   if (selectedIndex !== -1){
  //     var target_sentence = document.getElementById(selectedIndex);
  //     target_sentence.scrollIntoView({behavior: 'auto', block: 'nearest'})
  //   }
  // }, [selectedIndex]);
  
  const updateIndex = (currentTime) => {
    for (var i = 0; i < script.length; i++) {
      if (currentTime >= script[i]['start'] && currentTime <= script[i]['end']) {
        setSelectedIndex (i);
        return;
      }
    }
  }

  // video related
  const onGetCurrentTime = useCallback(() => {
    if (video === null) return 0;
    const currentTime = video.getCurrentTime().toFixed(3);
    updateIndex (currentTime);
    return currentTime;
  }, [video]);

  const onReady = (event) => {
      setVideo (event.target);
      setDuration (onGetDuration());
      // event.target.pauseVideo();
  };

  const onPause = () => {
    // logging
    setIsPlaying (false);
    logData ("pause", videoTime, {});
  }

  const onPlay = () => {
    // logging
    if (!isPlaying) {
      logData ("play", videoTime, {}, !started);
      setIsPlaying (true);
    };
    if (!started) {
      setStarted(true);
      setInitialTimeInfo (new Date().getTime() / 1000);
      const interval = setInterval(() => {
        const time = onGetCurrentTime();
        setVideoTime(time);
      }, 10);
      return () => {
        clearInterval(interval);
      };
    };
  };

  const onGetDuration = () => {
    if (video === null) return 0
    return video.getDuration();
  }

  const opts = {
  height: '500',
  width: '850',
  playerVars: {
      autoplay: 0,
      controls: 0,
      },
  };

  const showLabelInfo = (label) => {
    const trueLabel = labelInfo[label];
    const target = document.getElementById(trueLabel);
    target.style.visibility = "visible";
    target.parentElement.style.boxShadow = "0 0 25px rgb(34, 58, 164), 0 0 5px rgb(124, 144, 255)";
  };

  const hideLabelInfo = (label) => {
    const trueLabel = labelInfo[label];
    const target = document.getElementById(trueLabel);
    target.style.visibility = "";
    target.parentElement.style.boxShadow = "";
  };

  return (
    <div className="App">
      <Header 
        videoId={videoId}
        setVideoId={setVideoId}
        userId={userId}
        setUserId={setUserId}
        taskId={taskId}
        setTaskId={setTaskId}
      />
      <div>
        <Filter 
          colorPalette={colorPalette} 
          selectedLabels={selectedLabels} 
          setSelectedLabels={setSelectedLabels}
          />
      </div>
      <div className='body_wrapper'>
        <div className="video_wrapper">
          <YouTube 
              className='player'
              videoId={videoId} 
              opts={opts} 
              onReady={onReady}
              onPlay={onPlay}
              onPause={onPause}
          />
          <Timeline
            video={video}
            videoTime={videoTime}
            duration={duration}
            setVideoTime={setVideoTime}
            script={script}
            colorPalette={colorPalette}
            logData={logData}
            showLabelInfo={showLabelInfo}
            hideLabelInfo={hideLabelInfo}
            selectedLabels={selectedLabels}
            filteredScript={filteredScript}
          />
        </div>
        <div className='script_wrapper'>
          <Script 
            script={script}
            selectedIndex={selectedIndex}
            setSelectedIndex={setSelectedIndex}
            video={video}
            videoTime={videoTime}
            setVideoTime={setVideoTime}
            colorPalette={colorPalette}
            logData={logData}
            initialTimeInfo={initialTimeInfo}
            filteredScript={filteredScript}
            showLabelInfo={showLabelInfo}
            hideLabelInfo={hideLabelInfo}
          />
        </div>
      </div>
      {/* {hoverLabel && 
        <div className='info_wrapper'>
          <div style={{fontWeight: 500, backgroundColor: colorPalette[hoverLabel]}}>
            <span>{category[hoverLabel]}</span>
          </div>
          <div style={{marginTop: "5px"}}>
            {definition[hoverLabel]}
          </div>
        </div>
      } */}
    </div>
  );
}

export default App;
