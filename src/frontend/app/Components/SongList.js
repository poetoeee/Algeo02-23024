"use client";
import { useState, useEffect, useRef } from "react";

// Unified Card Component
const MediaCard = ({ item, onPlayPause, isAudioPlaying, isAudio }) => {
  return (
    <div className="relative bg-gray-800 text-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200">
      <div className="bg-gray-600 h-36 flex items-center justify-center">
        <img src={`http://127.0.0.1:8080/api/image/${isAudio ? item.imageUrl : item.name}`} alt="Media Art" className="h-full w-full object-cover" />
      </div>

      <div className="p-4">
        <p className="font-bold truncate">{isAudio ? item.name : item.audioUrl}</p>
        <p className="text-gray-400 text-sm">Similarity: {(item.kemiripan * 100).toFixed(2)}%</p>
      </div>

      <button onClick={() => onPlayPause(item)} className="absolute bottom-5 right-5 bg-white text-green-700 px-3 py-2 rounded-full hover:bg-green-600 hover:text-white">
        {isAudioPlaying ? "❚❚" : "▶"}
      </button>
    </div>
  );
};

const SongList = ({ lastSearch }) => {
  const [media, setMedia] = useState([]);
  const [songs, setSongs] = useState([]);
  const [imageMapping, setImageMapping] = useState([]);
  const [similarityMapping, setSimilarityMapping] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [currentPlayingItem, setCurrentPlayingItem] = useState(null);
  const [audio, setAudio] = useState(null);
  const [volume, setVolume] = useState(0.5);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);
  const [executionTime, setExecutionTime] = useState(null);
  const progressRef = useRef(null);

  const itemsPerPage = 18;

  useEffect(() => {
    const fetchExecutionTime = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8080/${lastSearch}/result/time.json`);
        if (!response.ok) {
          throw new Error("Failed to fetch execution time");
        }
        const data = await response.json();
        setExecutionTime(data.time);
      } catch (err) {
        console.error("Error fetching execution time:", err);
        setExecutionTime(null);
      }
    };

    fetchExecutionTime();
  }, [lastSearch]);

  useEffect(() => {
    const fetchSimilarityMapping = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8080/${lastSearch}/result/${lastSearch}.json`);
        if (!response.ok) {
          throw new Error("Failed to fetch similarity mapping");
        }
        const data = await response.json();
        setSimilarityMapping(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchSimilarityMapping();
  }, [lastSearch]);

  // Fetch image mapping
  useEffect(() => {
    const fetchImageMapping = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/api/images");
        if (!response.ok) {
          throw new Error("Failed to fetch image mapping");
        }
        const data = await response.json();
        setImageMapping(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchImageMapping();
  }, []);

  useEffect(() => {
    const fetchMedia = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/${lastSearch === "audio" ? "audios" : "imagess"}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch ${lastSearch}`);
        }
        const data = await response.json();

        const formattedMedia =
          lastSearch === "audio"
            ? data.songs.map((songFileName, index) => {
                const mappingItem = imageMapping.find((mapping) => mapping.audio_file === songFileName);
                return {
                  id: index + 1,
                  name: songFileName,
                  kemiripan: similarityMapping[songFileName] || 0,
                  imageUrl: mappingItem ? mappingItem.image_url : "",
                };
              })
            : data.images.map((imageFileName, index) => {
                const mappingItem = imageMapping.find((mapping) => mapping.image_url === imageFileName);
                return {
                  id: index + 1,
                  name: imageFileName,
                  kemiripan: similarityMapping[imageFileName] || 0,
                  audioUrl: mappingItem ? mappingItem.audio_file : "",
                };
              });

        console.log("Formatted Media:", formattedMedia);
        setMedia(formattedMedia);
      } catch (error) {
        console.error(`Error fetching ${lastSearch}:`, error);
      } finally {
        setLoading(false);
      }
    };

    if (Object.keys(similarityMapping).length > 0 && imageMapping.length > 0) {
      fetchMedia();
    }
  }, [similarityMapping, imageMapping, lastSearch]);

  // useEffect(() => {
  //   if (!Object.keys(similarityMapping).length || !imageMapping.length) return;

  //   const formattedMedia = Object.entries(similarityMapping).map(([key, kemiripan], index) => {
  //     const mappingItem = imageMapping.find((mapping) => (lastSearch === "audio" ? mapping.audio_file === key : mapping.image_url === key));

  //     return {
  //       id: index + 1,
  //       name: key,
  //       kemiripan,
  //       imageUrl: mappingItem?.image_url || "",
  //       audioUrl: mappingItem?.audio_file || "",
  //     };
  //   });

  //   setMedia(formattedMedia);
  // }, [similarityMapping, imageMapping, lastSearch]);

  const handlePlayPause = (item) => {
    if (currentPlayingItem?.name === item.name) {
      if (audio?.paused) {
        audio.play();
        setIsAudioPlaying(true);
      } else {
        audio.pause();
        setIsAudioPlaying(false);
      }
    } else {
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
        setCurrentPlayingItem(null);
      }

      const newAudio = new Audio(`http://127.0.0.1:8080/api/play/${item.name}`);
      newAudio.volume = volume;

      newAudio.addEventListener("timeupdate", () => {
        if (progressRef.current) {
          progressRef.current.value = (newAudio.currentTime / newAudio.duration) * 100;
        }
      });

      newAudio.addEventListener("ended", () => {
        setCurrentPlayingItem(null);
        setIsAudioPlaying(false);
      });

      setAudio(newAudio);
      setCurrentPlayingItem(item);
      setIsAudioPlaying(true);
      newAudio.play();
    }
  };

  const handleVolumeChange = (event) => {
    const newVolume = event.target.value / 100;
    setVolume(newVolume);
    if (audio) audio.volume = newVolume;
  };

  const handleProgressChange = (event) => {
    const newTime = (event.target.value / 100) * audio.duration;
    audio.currentTime = newTime;
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = media
    .filter((item) => item.kemiripan > 0)
    .sort((a, b) => b.kemiripan - a.kemiripan)
    .slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil(media.length / itemsPerPage);

  if (loading) {
    return <div className="text-center text-gray-600 mt-10">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-600 mt-10">{error}</div>;
  }

  return (
    <div className="p-5">
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
        {currentItems.length > 0 ? (
          currentItems.map((item) => <MediaCard key={item.id} item={item} onPlayPause={handlePlayPause} isAudioPlaying={currentPlayingItem?.name === item.name && !audio?.paused} isAudio={lastSearch === "audio"} />)
        ) : (
          <div className="text-gray-600 text-center col-span-full">No media found for "{lastSearch}".</div>
        )}
      </div>

      <div className="flex justify-center items-center mt-6 space-x-4">
        <button onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} className="px-4 py-2 rounded bg-green-700 hover:bg-green-800 text-white">
          Prev
        </button>
        <button onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))} className="px-4 py-2 rounded bg-green-700 hover:bg-green-800 text-white">
          Next
        </button>
      </div>

      {executionTime && (
        <div className="text-center text-gray-600 mt-6">
          <p>Execution Time: {parseFloat(executionTime).toFixed(2)} seconds</p>
        </div>
      )}

      {currentPlayingItem && (
        <div className="fixed bottom-0 left-0 w-full bg-gray-700 text-white p-4 flex justify-between items-center">
          <p className="font-bold mr-4">{currentPlayingItem.name}</p>
          <input type="range" min="0" max="100" ref={progressRef} onChange={handleProgressChange} className="w-3/5 mx-4" />
          <input type="range" min="0" max="100" value={volume * 100} onChange={handleVolumeChange} className="w-1/6" />
        </div>
      )}
    </div>
  );
};

export default SongList;
