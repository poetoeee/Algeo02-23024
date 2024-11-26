import { useState } from "react";

const Search = ({ setSearch }) => {
  const [isVisible, setIsVisible] = useState(false);

  const handleSearchChange = (searchValue) => {
    setSearch(searchValue);
    setIsVisible(searchValue.trim() !== "");
  };

  return (
    <input
      type="text"
      placeholder="Search by name"
      className="w-full sm:w-3/4 md:w-3/4 lg:w-3/5 xl:w-3/5 p-4 rounded-[20px] max-h-[46px] border border-[#ddd] text-base text-black mb-4 mt-5"
      onChange={({ currentTarget: input }) => handleSearchChange(input.value)}
    />
  );
};

export default Search;
