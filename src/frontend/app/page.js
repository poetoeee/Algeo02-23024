"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Search from "./Components/Search";
import Sidebar from "./Components/Sidebar";

function App() {
  const [searchValue, setSearchValue] = useState("");

  const handleSearchChange = (value) => {
    setSearchValue(value);
    console.log("Search Value:", value);
  };

  return (
    <div className="flex flex-col bg-gray-100 min-h-screen max-w-full">
      <div className="bg-black shadow flex items-center justify-between px-4">
        <h1 className="text-white text-2xl font-bold">Audio Searcher</h1>
        <div className="flex-1 flex justify-center">
          <Search setSearch={handleSearchChange} />
        </div>
      </div>
      <div className="flex flex-row flex-1">
        <Sidebar />
        <div className="flex-1 p-5">
          <div className="flex justify-center mb-5">
            <button className="px-10 py-2 bg-gray-700 text-white rounded-l-md focus:outline-none hover:bg-gray-800">Album</button>
            <button className="px-10 py-2 bg-gray-600 text-white rounded-r-md focus:outline-none hover:bg-gray-800">Music</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
