import React, { useState, useEffect, useCallback } from 'react'
import db from "./service/firebase";
import { ref, set, get } from "firebase/database";
import YouTube from 'react-youtube';
import './App.css';

// components
import Header from './components/Header';
import Script from './components/Script';
import Timeline from './components/Timeline';

function App() {
  const [video, setVideo] = useState (null);
  const [started, setStarted] = useState(false);

  const [videoId, setVideoId] = useState ('Eeu5uL6r2rg');
  const [videoTime, setVideoTime] = useState (0);
  const [duration, setDuration] = useState (0);

  const [scriptLoaded, setScriptLoaded] = useState (false);
  const [script, setScript] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState (-1);

  // for log
  // Task Id
  // 0 for search, 1 for skim and summary, 2 for following
  const [userId, setUserId] = useState("");
  const [taskId, setTaskId] = useState("");
  const [initialTimeInfo, setInitialTimeInfo] = useState (null);

   // colors
  const colorPalette = {
    // high-level type
    'greeting':'yellow',
    'overview':'green ',
    'step':'purple',
    'supplementary':'white',
    'explanation':'lightblue',
    'description':'yellow',
    'conclusion':'blue',
    'misc.':'lightcyan',
    
    // low-level type
    //greeting
    'opening':'#DAF283',
    //overview
    'goal': '#F6BD60',
    'motivation':'#F6BD60',
    'briefing':'#F6BD60',
    //step
    'subgoal':'#F5A7A6 ',
    'instruction':'#F5A7A6',
    'tool':'#F5A7A6',
    'tool (multiple)':'#F5A7A6',
    'tool (optional)':'#F5A7A6',
    //explanation
    'justification':'#FFF5AB',
    'effect':'#FFF5AB',
    //supplementary
    'warning':'#C7B4C4',
    'tip':'#C7B4C4',
    //description
    'status':'#A8D0C6',
    'context':'#A8D0C6',
    'tool spec.':'#A8D0C6',
    //greeting-outro
    'closing':'#DAF283',
    //conclusion
    'outcome':'#DCC8E6',
    'reflection':'#DCC8E6',
    //misc
    'side note':'lightgray',
    'self-promo':'lightgray',
    'bridge':'lightgray',
    'filler':'lightgray'
}

  // database
  const logData=(action, video_ts, user_ts, meta)=>{
    console.log (videoId, userId, taskId);
    if (videoId === "" || userId === "" || taskId === "") return;

    set(ref(db, '/Log' + '/' + userId + '/' + videoId + '/' + taskId), {
      action: action, // pause, play, jump
      video_timestamp: video_ts,
      user_timestamp: user_ts, 
      meta: meta // optional, format: {source: keyboard/click, location: playbar/script}
    });
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
      });
  };

  useEffect(()=>{
    getScript();
  }, [videoId]);


  const onKeyPress = (e) => {
    const keyCode = e.keyCode;
    let ind, vt;
    if (keyCode == 38) {  // up arrow
        if (selectedIndex > 0) {
          ind = selectedIndex-1;
          handleIndexChange (ind);
        } 
      } else if (keyCode == 40) { // down arrow
        if (selectedIndex < script.length-1) {
          ind = selectedIndex+1;
          handleIndexChange (ind);
        }
    } else if (keyCode == 37) {
      vt = videoTime - 5;
      setVideoTime (vt);
      video.seekTo (vt);
    } else if (keyCode == 39) {
      vt = videoTime + 5;
      setVideoTime (vt);
      video.seekTo (vt);
    }
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


  // video related
  const onGetCurrentTime = useCallback(() => {
    if (video === null) return 0;
    const currentTime = Math.floor(video.getCurrentTime()); //int
    return currentTime;
  }, [video]);

  const onReady = (event) => {
      setVideo (event.target);
      setDuration (onGetDuration());
      // event.target.pauseVideo();
  };

  const onPlay = () => {
    if (!started) {
      setStarted(true);
      setInitialTimeInfo (new Date().getTime());
      const interval = setInterval(() => {
        const time = onGetCurrentTime();
        setVideoTime(time);
      }, 1000);
      return () => {
        clearInterval(interval);
      };
    }
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
      },
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
      <div className='body_wrapper'>
        <div className="video_wrapper">
          <YouTube 
              className='player'
              videoId={videoId} 
              opts={opts} 
              onReady={onReady}
              onPlay={onPlay}
          />
          <Timeline
            video={video}
            videoTime={videoTime}
            duration={duration}
            setVideoTime={setVideoTime}
            script={script}
            colorPalette={colorPalette}
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
          />
        </div>
      </div>
    </div>
  );
}

export default App;
