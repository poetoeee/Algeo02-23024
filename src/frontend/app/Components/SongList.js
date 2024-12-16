"use client";
import { useState, useEffect, useRef } from "react";

// SongCard Component
const SongCard = ({ song, onPlayPause, isAudioPlaying }) => {
  return (
    <div className="relative bg-gray-800 text-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200">
      <div className="bg-gray-600 h-36 flex items-center justify-center">
        <img src={`http://127.0.0.1:8080${song.imageUrl}`} alt="Album Art" className="h-full w-full object-cover" />
      </div>

      <div className="p-4">
        <p className="font-bold truncate">{song.name}</p>
        <p className="text-gray-400 text-sm">Similarity: {(song.kemiripan * 100).toFixed(2)}%</p>
      </div>

      <button onClick={() => onPlayPause(song)} className="absolute bottom-5 right-5 bg-white text-green-700 px-3 py-2 rounded-full hover:bg-green-600 hover:text-white">
        {isAudioPlaying ? "❚❚" : "▶"}
      </button>
    </div>
  );
};

const SongList = () => {
  const [songs, setSongs] = useState([]);
  const [imageMapping, setImageMapping] = useState([]);
  const [similarityMapping, setSimilarityMapping] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [currentPlayingSong, setCurrentPlayingSong] = useState(null);
  const [audio, setAudio] = useState(null);
  const [volume, setVolume] = useState(0.5); // Default volume 100%
  const [isLooping, setIsLooping] = useState(false);
  const [isShuffling, setIsShuffling] = useState(false);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);
  const progressRef = useRef(null);

  const itemsPerPage = 18;

  useEffect(() => {
    const fetchSimilarityMapping = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/audio/result/audio.json");
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
  }, []);

  // Fetch image mapping from backend
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

  // Fetch songs from backend API
  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/api/audios");
        if (!response.ok) {
          throw new Error("Failed to fetch songs");
        }
        const data = await response.json();

        const formattedSongs = data.songs.map((songFileName, index) => {
          const imageMappingItem = imageMapping.find((mapping) => mapping.audio_file === songFileName);
          return {
            id: index + 1,
            name: songFileName,
            kemiripan: similarityMapping[songFileName] || 0,
            imageUrl: imageMappingItem ? imageMappingItem.image_url : "",
          };
        });

        setSongs(formattedSongs);
      } catch (error) {
        console.error("Error fetching songs:", error);
      } finally {
        setLoading(false);
      }
    };

    if (Object.keys(similarityMapping).length > 0 && imageMapping.length > 0) {
      fetchSongs();
    }
  }, [similarityMapping, imageMapping]);

  const handlePlayPause = (song) => {
    if (currentPlayingSong?.name === song.name) {
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
        setCurrentPlayingSong(null);
      }

      const newAudio = new Audio(`http://127.0.0.1:8080/api/play/${song.name}`);
      newAudio.volume = volume;
      newAudio.loop = isLooping;

      newAudio.addEventListener("timeupdate", () => {
        if (progressRef.current) {
          progressRef.current.value = (newAudio.currentTime / newAudio.duration) * 100;
        }
      });

      newAudio.addEventListener("ended", () => {
        if (isShuffling) {
          const nextIndex = Math.floor(Math.random() * songs.length);
          handlePlayPause(songs[nextIndex]);
        } else {
          setCurrentPlayingSong(null);
        }
      });

      setAudio(newAudio);
      setCurrentPlayingSong(song);
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

  const toggleLoop = () => setIsLooping((prev) => !prev);
  const toggleShuffle = () => setIsShuffling((prev) => !prev);

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = songs.slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil(songs.length / itemsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage((prev) => prev + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  if (loading) {
    return <div className="text-center text-gray-600 mt-10">Loading...</div>;
  }
  if (error) return <div className="text-center text-red-600 mt-10">{error}</div>;

  return (
    <div className="p-5">
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
        {currentItems.map((song) => (
          <SongCard key={song.id} song={song} onPlayPause={handlePlayPause} isAudioPlaying={currentPlayingSong?.name === song.name && !audio?.paused} />
        ))}
      </div>

      <div className="flex justify-center items-center mt-6 space-x-4">
        <button onClick={handlePreviousPage} disabled={currentPage === 1} className={`px-4 py-2 rounded ${currentPage === 1 ? "bg-gray-400 cursor-not-allowed" : "bg-green-700 hover:bg-green-800 text-white"}`}>
          Prev
        </button>

        <div className="flex items-center space-x-2">
          {[...Array(totalPages)].map((_, index) => (
            <button
              key={index + 1}
              onClick={() => setCurrentPage(index + 1)}
              className={`w-8 h-8 rounded-full flex items-center justify-center ${currentPage === index + 1 ? "bg-green-700 text-white" : "bg-gray-300 hover:bg-green-600 text-black"}`}
            >
              {index + 1}
            </button>
          ))}
        </div>

        <button onClick={handleNextPage} disabled={currentPage === totalPages} className={`px-4 py-2 rounded ${currentPage === totalPages ? "bg-gray-400 cursor-not-allowed" : "bg-green-700 hover:bg-green-800 text-white"}`}>
          Next
        </button>
      </div>

      {currentPlayingSong && (
        <div className="fixed bottom-0 left-0 w-full bg-gray-700 text-white p-4 flex justify-between items-center">
          <div className="flex items-center">
            <p className="font-bold mr-4">{currentPlayingSong.name}</p>
            <button onClick={toggleLoop} className={`px-2 transition-all duration-300 ${isLooping ? "text-green-400 scale-150" : "text-white scale-110"}`}>
              🔁
            </button>
            <button onClick={toggleShuffle} className={`px-2 transition-all duration-300 ${isShuffling ? "text-green-400 scale-150" : "text-white scale-110"}`}>
              🔀
            </button>
          </div>

          <input type="range" min="0" max="100" ref={progressRef} onChange={handleProgressChange} className="w-3/5 mx-4" />

          <input type="range" min="0" max="100" value={volume * 100} onChange={handleVolumeChange} className="w-1/6" />
        </div>
      )}
    </div>
  );
};

export default SongList;
