"use client";
import { useState, useRef } from "react";

const uploadOptions = [
  { type: "Audios", accept: ".zip" },
  { type: "Pictures", accept: ".zip" },
  { type: "Mapper", accept: ".txt" },
];

const Sidebar = () => {
  const [selectedFiles, setSelectedFiles] = useState({
    Audios: "-",
    Pictures: "-",
    Mapper: "-",
  });
  const [currentUploadType, setCurrentUploadType] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const allowedType = uploadOptions.find((option) => option.type === currentUploadType)?.accept;

    if (allowedType && !file.name.endsWith(allowedType)) {
      alert(`Invalid file type! Only ${allowedType} files are allowed.`);
      return;
    }

    setSelectedFiles((prevFiles) => ({
      ...prevFiles,
      [currentUploadType]: file.name,
    }));
  };

  const handleUploadClick = (uploadType) => {
    setCurrentUploadType(uploadType);
    fileInputRef.current.click();
  };

  return (
    <div className="w-1/5 h-screen bg-gray-900 text-white p-10 flex flex-col">
      <h1 className="text-5xl font-bold mb-10">HOREG 2.0</h1>

      <div className="bg-gray-800 p-4 rounded mt-10 mb-20">
        <h3 className="text-lg font-bold mb-3">Upload File</h3>

        {selectedFiles.Upload && selectedFiles.Upload !== "-" && <p className="text-sm text-gray-300 mb-2">{selectedFiles.Upload}</p>}

        <input
          type="file"
          ref={fileInputRef}
          onChange={(event) => {
            const file = event.target.files[0];
            if (file) {
              setSelectedFiles((prev) => ({
                ...prev,
                Upload: file.name,
              }));
            }
          }}
          className="hidden"
        />

        <button onClick={() => handleUploadClick("Upload")} className="w-full px-4 py-2 bg-green-700 text-white rounded hover:bg-green-800">
          Upload
        </button>
      </div>

      <ul className="list-none space-y-4 mb-10 mt-20">
        {uploadOptions.map((option) => (
          <li key={option.type}>
            <button onClick={() => handleUploadClick(option.type)} className="w-full text-center px-4 py-2 rounded bg-gray-800 hover:bg-gray-700">
              {option.type}
            </button>
          </li>
        ))}
      </ul>

      <div className="grid grid-cols-[30%_5%_65%] gap-2">
        <p className="text-lg font-bold">Audios</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Audios}</p>
        <p className="text-lg font-bold">Pictures</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Pictures}</p>
        <p className="text-lg font-bold">Mapper</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Mapper}</p>
      </div>
    </div>
  );
};

export default Sidebar;
