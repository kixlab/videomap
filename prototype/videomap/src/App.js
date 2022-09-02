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

  const [videoId, setVideoId] = useState ('_Yb6xLqvsf0');
  const [videoTime, setVideoTime] = useState (0);
  const [duration, setDuration] = useState (0);

  const [scriptLoaded, setScriptLoaded] = useState (false);
  const [script, setScript] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState (-1);

  // filter
  const [selectedLabels, setSelectedLabels] = useState (["opening", "goal", "motivation", "briefing", "subgoal", "instruction", "tool", "justification", "effect", "tip", "warning", "status", "context", "tool-spec", "closing", "outcome", "reflection", "side-note", "self-promo", "bridge", "filler"]);
  const [filteredScript, setFilteredScript] = useState ([]);
  const [processedScript, setProcessedScript] = useState([]);

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
    const user_timestamp = (firstLog || !started) ? 0 : (new Date().getTime() / 1000 - initialTimeInfo).toFixed(3);
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
        setScriptLoaded (true);
        // filter
        processScript (jsonFile);
      });
  };

  useEffect(()=>{
    getScript();
  }, [videoId]);

  // filter script
  const processScript = (inputScript=[]) => {
    const useScript = inputScript.length == 0 ? script : inputScript;
    const processed = useScript.map (item => {
        if (selectedLabels.includes (labelInfo[item.low_label])) item['use'] = true;
        else item['use'] = false;
        return item;
    });
    const filtered = processed.filter (item => item.use == true);
    const newIndex = filtered.length > 0 ? filtered[0].index : -1;

    setProcessedScript (processed);
    setFilteredScript (filtered);
    setSelectedIndex (newIndex);
  }

  useEffect(() => {
    if (script.length > 0) {
        // filterScript();
        processScript();
    }
  }, [videoId, selectedLabels])

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
    // logging
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
      // setVideoTime (vt);
      video.seekTo (vt);

    // right arrow
    } else if (keyCode == 39) {
      // logging
      logKeyPress ("right", ind);
      vt = (parseFloat(videoTime) + 5).toFixed(3);
      // setVideoTime (vt);
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
    // setVideoTime (script[index].start);
    video.seekTo (script[index].start);
  };

  useEffect(() => {
    if (video && scriptLoaded) {
      document.addEventListener('keydown', onKeyPress);
      return function cleanup() {
        document.removeEventListener('keydown', onKeyPress);
      }
    };
  }, [video, videoTime, scriptLoaded, selectedIndex]);

  useEffect(() => {
    if (video && selectedIndex !== -1){
      var target_sentence = document.getElementsByClassName(selectedIndex)[0];
      target_sentence.scrollIntoView({behavior: 'auto', block: 'nearest'});
      // setVideoTime (script[selectedIndex].start);
      // video.seekTo (script[selectedIndex].start);
    }
    
  }, [selectedIndex]);
  
  const updateIndex = () => {
    for (var i = 0; i < filteredScript.length; i++) {
      if (videoTime >= filteredScript[i]['start'] && videoTime <= filteredScript[i]['end'] && filteredScript[i].index != selectedIndex ) {
        setSelectedIndex (filteredScript[i].index);
        return;
      }
    }
  }

  // video related
  const onGetCurrentTime = useCallback(() => {
    if (video === null) return 0;
    const currentTime = video.getCurrentTime().toFixed(3);
    return currentTime;
  }, [video]);

  const onReady = (event) => {
    setVideo (event.target);
    setDuration (onGetDuration());
  };

  const onPause = () => {
    // logging
    setIsPlaying (false);
    logData ("pause", videoTime, {});
  }

  const getIndexWithTime = (time) => {
    // when time is lower than the first element starting
    if (time < processedScript[0].start) return [0, true];

    for (var i=0; i<processedScript.length; i++) {
      if (processedScript[i].start <= time && processedScript[i].next_start >= time) {
        if (processedScript[i].use) {
          return [i, true];
        } else {
          var ind = i+1;
          while (ind < processedScript.length && !processedScript[ind].use) {
            ind += 1;
          }
          return [ind, false];
        }
      }
    }
  };

  const jumpTime = (time) => {
    // last segment in the filtered script
    var indArr = getIndexWithTime (time);
    var selInd = indArr[0];
    var inUse = indArr[1];

    if (inUse) {
      // play 되지 말아야할 초과 index -> 바로 멈춤
      if (selInd > filteredScript[filteredScript.length-1].index) {
        setIsPlaying (false);
        video.pauseVideo();
        return;
      }

      // play 되어야할 마지막 index -> 시간이 넘으면 멈춤
      if (selInd == filteredScript[filteredScript.length-1].index) {
        if (time >= processedScript[selInd].next_start) {
          setIsPlaying (false);
          video.pauseVideo();
          return;
        }
      }

      // 마지막 index가 아니고, 다음꺼도 사용한다 -> jump하지 말고 return 해라
      if (selInd < filteredScript.length-1 && processedScript[selInd+1].use) {
        return;
      } 

      // 지금 index에서 이제 시간이 끝남 -> 다음 play할 index를 찾아라
      if (processedScript[selInd].next_start <= time){
        var ind = selInd + 1;
        while (!processedScript[ind].use) {
          ind += 1;
        }
        if (processedScript[ind].start > time) {
          const vt = processedScript[ind].start;
          video.seekTo (vt);
        }
      }
    } else {
      // play 되지 말아야할 초과 index -> 바로 멈춤
      if (selInd > filteredScript[filteredScript.length-1].index) {
        setIsPlaying (false);
        video.pauseVideo();
        return;
      }
      const vt = processedScript[selInd].start;
      video.seekTo (vt);
    }
  };

  useEffect (()=>{
    updateIndex();
  },[videoTime])

  // on every video time change, call jumptime
  useEffect (() => {
    if (filteredScript.length > 0 && isPlaying) {
      jumpTime (videoTime);
    }
  }, [videoTime, filteredScript, processedScript, selectedLabels]);

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
        setVideoTime (time);
      }, 10);
      return () => {
        clearInterval(interval);
      };
    };
  };

  const onGetDuration = () => {
    if (video === null) return 0;
    return video.getDuration();
  }

  const opts = {
  height: '500',
  width: '850',
  playerVars: {
      autoplay: 0,
      controls: 1,
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
          logData={logData}
          videoTime={videoTime}
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
            videoId={videoId}
            videoTime={videoTime}
            duration={duration}
            setVideoTime={setVideoTime}
            colorPalette={colorPalette}
            logData={logData}
            showLabelInfo={showLabelInfo}
            hideLabelInfo={hideLabelInfo}
            selectedLabels={selectedLabels}
            processedScript={processedScript}
            setSelectedIndex={setSelectedIndex}
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
