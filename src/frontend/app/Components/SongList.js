"use client";

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
  ];

  return (
    <div className="grid grid-cols-4 gap-6 p-5">
      {dummySongs.map((song) => (
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
  );
};

export default SongList;
