"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Search from "./Components/Search";
import Sidebar from "./Components/Sidebar";
import SongList from "./Components/SongList";

const App = () => {
  const [lastSearch, setLastSearch] = useState("audio");

  const handleSearchChange = (value) => {
    setSearchValue(value);
    console.log("Search Value:", value);
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar setLastSearch={setLastSearch} />
      <div className="flex-1 p-5">
        {/* <div className="flex justify-center mb-2 mt-1">
          <button className="px-10 py-2 bg-gray-700 text-white rounded-l-md focus:outline-none hover:bg-gray-800">Album</button>
          <button className="px-10 py-2 bg-gray-600 text-white rounded-r-md focus:outline-none ${isActive ? 'bg-green-700' : ''}">Music</button>
        </div> */}
        <SongList lastSearch={lastSearch} />
      </div>
    </div>
  );
};

export default App;
