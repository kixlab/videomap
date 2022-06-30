const youtubedl = require('youtube-dl-exec');
const {readFileSync, writeFileSync, promises: fsPromises} = require('fs');

async function getDuration(video_id) {
    video_url = "youtu.be/" + video_id
    var duration = 0;

    await youtubedl(video_url, {
      getDuration: true,
    }).then(output => duration = output)
    .catch((err) => {
      duration = "error";
      // console.log(err)
    });
    
    return duration
}

async function getDate(video_id) {
    video_url = "youtu.be/" + video_id
    var date = 0;

    await youtubedl(video_url, {
      dumpSingleJson: true,
    }).then(output => date = output['upload_date'])
    .catch((err) => {
      date = "error";
      // console.log(err)
    });

    return date
}

function writeFile (index, content) {
  writeFileSync('HowTo100M_info_'+index+'.txt', content, err => {
    if (err) {
      console.error(err)
      return
    }
  })
}

async function syncReadFile(filename) {
    const content = readFileSync(filename, 'utf-8');
    const content_list = content.split(/\r?\n/);
    var write_content = "";
    for (var i=700000; i>=0; i--){
      if (i % 1000 == 0) {
        if (i == 700000) {
          continue
        }
        writeFile(i, write_content)
        var write_content = "";
        console.log (i)
      }
      var j = content_list[i].indexOf(',')
      var video_id = content_list[i].substring(0, j)
      var category = content_list[i].substring(j+2,)
      // console.log(video_id)
      var duration;
      var date;
      duration = await getDuration(video_id)
      date = await getDate(video_id)
      write_content += video_id + ", " + category + ", " + duration + ", " + date
      write_content += "\n"
      // console.log(duration)
      // console.log(date)
    }

  }
  
  syncReadFile('./data/HowTo100M_v1.txt');
