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

  const [scriptLoaded, setScriptLoaded] = useState (false);

  const [videoId, setVideoId] = useState ('Eeu5uL6r2rg');
  const [videoTime, setVideoTime] = useState (0);
  const [duration, setDuration] = useState (0);

  const [script, setScript] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState (-1);

  // database
  const logData=(userId, name, email)=>{
    set(ref(db, '/' + userId), {
      username: name,
      email: email,
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
          handleIndexChange (ind)
        } 
      } else if (keyCode == 40) { // down arrow
        if (selectedIndex < script.length-1) {
          ind = selectedIndex+1;
          handleIndexChange (ind)
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
      autoplay: 1,
      },
  };

  return (
    <div className="App">
      <Header 
        videoId={videoId}
        setVideoId={setVideoId}
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
          />
        </div>
      </div>
    </div>
  );
}

export default App;
