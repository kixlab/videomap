import React, { useState, useEffect, useCallback } from 'react'
import YouTube from 'react-youtube';
import './App.css';

// components
import Header from './components/Header';
import Script from './components/Script';

function App() {
  const [video, setVideo] = useState (null);
  const [started, setStarted] = useState(false);

  const [scriptLoaded, setScriptLoaded] = useState (false);

  const [videoId, setVideoId] = useState ('mQjCKgEPs8k');
  const [videoTime, setVideoTime] = useState (0);

  const [script, setScript] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState (-1);
  
  const getData=()=>{
    fetch(process.env.PUBLIC_URL + `/data/${videoId}.json`)
      .then(function (response){
        return response.json();
      })
      .then(function (jsonFile) {
        setScript (jsonFile);
        setSelectedIndex (0);
        setScriptLoaded (true);
      });
  }

  useEffect(()=>{
    getData()
  }, [videoId])

  const onKeyPress = (e) => {
    console.log (e.keyCode)
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
    setSelectedIndex (index)
    setVideoTime (script[index].Start)
    video.seekTo (script[index].Start)
  };

  useEffect(() => {
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

  const opts = {
  height: '468',
  width: '768',
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
      <div className="video_wrapper">
        <YouTube 
            videoId={videoId} 
            opts={opts} 
            onReady={onReady}
            onPlay={onPlay}
        />
      </div>
      <Script 
        script={script}
        selectedIndex={selectedIndex}
        setSelectedIndex={setSelectedIndex}
        video={video}
        videoTime={videoTime}
        setVideoTime={setVideoTime}
      />
    </div>
  );
}

export default App;
