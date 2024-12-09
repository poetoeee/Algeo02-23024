"use client";
import { useState } from "react";

const SongList = () => {
  const dummySongs = [
    { id: 1, name: "audio1.wav", album: "Album 1", kemiripan: "0" },
    { id: 2, name: "audio2.wav", album: "Album 2", kemiripan: "0" },
    { id: 3, name: "audio3.wav", album: "Album 3", kemiripan: "0" },
    { id: 4, name: "audio4.wav", album: "Album 4", kemiripan: "0" },
    { id: 5, name: "audio5.wav", album: "Album 5", kemiripan: "0" },
    { id: 6, name: "audio6.wav", album: "Album 6", kemiripan: "0" },
    { id: 7, name: "audio7.wav", album: "Album 7", kemiripan: "0" },
    { id: 8, name: "audio8.wav", album: "Album 8", kemiripan: "0" },
    { id: 9, name: "audio9.wav", album: "Album 9", kemiripan: "0" },
    { id: 10, name: "audio10.wav", album: "Album 10", kemiripan: "0" },
    { id: 11, name: "audio11.wav", album: "Album 11", kemiripan: "0" },
    { id: 12, name: "audio12.wav", album: "Album 12", kemiripan: "0" },
    { id: 13, name: "audio13.wav", album: "Album 13", kemiripan: "0" },
    { id: 14, name: "audio14.wav", album: "Album 14", kemiripan: "0" },
    { id: 15, name: "audio15.wav", album: "Album 15", kemiripan: "0" },
    { id: 16, name: "audio16.wav", album: "Album 16", kemiripan: "0" },
    { id: 17, name: "audio17.wav", album: "Album 17", kemiripan: "0" },
    { id: 18, name: "audio18.wav", album: "Album 18", kemiripan: "0" },
    { id: 19, name: "audio19.wav", album: "Album 19", kemiripan: "0" },
    { id: 20, name: "audio20.wav", album: "Album 20", kemiripan: "0" },
    { id: 21, name: "audio21.wav", album: "Album 21", kemiripan: "0" },
    { id: 22, name: "audio22.wav", album: "Album 22", kemiripan: "0" },
    { id: 23, name: "audio23.wav", album: "Album 23", kemiripan: "0" },
    { id: 24, name: "audio24.wav", album: "Album 24", kemiripan: "0" },
    { id: 25, name: "audio25.wav", album: "Album 25", kemiripan: "0" },
    { id: 26, name: "audio26.wav", album: "Album 26", kemiripan: "0" },
  ];

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 12;

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = dummySongs.slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil(dummySongs.length / itemsPerPage);

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

  return (
    <div>
      <div className="grid grid-cols-4 gap-6 p-5">
        {currentItems.map((song) => (
          <div key={song.id} className="relative bg-gray-800 text-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200">
            <div className="bg-gray-600 h-36 flex items-center justify-center">
              <p className="text-gray-400 text-sm">Album Art</p>
            </div>

            <div className="p-4">
              <p className="font-bold truncate">{song.name}</p>
              <p className="text-gray-400 text-sm truncate">{song.kemiripan}%</p>
            </div>

            <button className="absolute bottom-5 right-5 bg-white text-green-700 px-3 py-2 rounded-full hover:bg-green-600 hover:text-white">▶</button>
          </div>
        ))}
      </div>

      <div className="absolute bottom-5 left-[50%] translate-x-[20%] flex justify-center items-center space-x-4">
        <button onClick={handlePreviousPage} disabled={currentPage === 1} className={`px-4 py-2 rounded ${currentPage === 1 ? "bg-gray-400 cursor-not-allowed" : "bg-green-700 hover:bg-green-800 text-white"}`}>
          Prev
        </button>
        <p className="text-black">
          Page {currentPage} of {totalPages}
        </p>
        <button onClick={handleNextPage} disabled={currentPage === totalPages} className={`px-4 py-2 rounded ${currentPage === totalPages ? "bg-gray-400 cursor-not-allowed" : "bg-green-700 hover:bg-green-800 text-white"}`}>
          Next
        </button>
      </div>
    </div>
  );
};

export default SongList;
