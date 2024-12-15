"use client";
import { useState, useEffect } from "react";

// SongCard Component
const SongCard = ({ song }) => {
  return (
    <div className="relative bg-gray-800 text-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200">
      <div className="bg-gray-600 h-36 flex items-center justify-center">
        {/* Placeholder for Album Art */}
        <img
          src={`http://127.0.0.1:8080${song.imageUrl}`} // Default image if imageUrl is missing
          alt="Album Art"
          className="h-full w-full object-cover"
        />
      </div>

      <div className="p-4">
        <p className="font-bold truncate">{song.name}</p>
        <p className="text-gray-400 text-sm">Similarity: {song.kemiripan}%</p>
      </div>

      <button className="absolute bottom-5 right-5 bg-white text-green-700 px-3 py-2 rounded-full hover:bg-green-600 hover:text-white">▶</button>
    </div>
  );
};

const SongList = () => {
  const [songs, setSongs] = useState([]);
  const [imageMapping, setImageMapping] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 18;

  // Fetch Gambar Mapping dari Backend
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

  // Fetch Songs from Backend API
  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/api/audios");
        if (!response.ok) {
          throw new Error("Failed to fetch songs");
        }
        const data = await response.json();

        // Convert songs array into objects with name property
        const formattedSongs = data.songs.map((songFileName, index) => {
          const imageMappingItem = imageMapping.find((mapping) => mapping.audio_file === songFileName);
          return {
            id: index + 1,
            name: songFileName, // Use the filename as the name
            album: "", // Placeholder for album if not provided
            kemiripan: "0", // Default similarity
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

    fetchSongs();
  }, [imageMapping]);

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
      {/* Song Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
        {currentItems.map((song) => (
          <SongCard key={song.id} song={song} />
        ))}
      </div>

      {/* Pagination Controls */}
      <div className="flex justify-center items-center mt-6 space-x-4">
        <button onClick={handlePreviousPage} disabled={currentPage === 1} className={`px-4 py-2 rounded ${currentPage === 1 ? "bg-gray-400 cursor-not-allowed" : "bg-green-700 hover:bg-green-800 text-white"}`}>
          Prev
        </button>

        {/* Current Page Indicator */}
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
    </div>
  );
};

export default SongList;
