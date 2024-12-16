"use client";
import { useState, useRef } from "react";

const uploadOptions = [
  { type: "Audio", endpoint: "/api/upload_query_song", accept: ".mid", field: "file_song" },
  { type: "Image", endpoint: "/api/upload_query_image", accept: ".jpg,.jpeg,.png", field: "file_image" },
  { type: "Audios", endpoint: "/api/upload_song", accept: ".zip", field: "file_song_db" },
  { type: "Images", endpoint: "/api/upload_image", accept: ".zip", field: "file_image_db" },
  { type: "Mapper", accept: ".json" },
];

const Sidebar = () => {
  const [selectedFiles, setSelectedFiles] = useState({
    Audio: "-",
    Image: "-",
    Audios: "-",
    Images: "-",
    Mapper: "-",
  });
  const fileInputRef = useRef(null);
  const currentUploadTypeRef = useRef(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    const uploadType = currentUploadTypeRef.current;
    if (!file || !uploadType) return;

    const uploadOption = uploadOptions.find((option) => option.type === uploadType);
    if (!uploadOption) {
      console.error("Upload option not found.");
      return;
    }

    const allowedExtensions = uploadOption.accept.split(",");
    const isAllowed = allowedExtensions.some((ext) => file.name.toLowerCase().endsWith(ext));
    if (!isAllowed) {
      alert(`Invalid file type! Only ${allowedExtensions.join(", ")} files are allowed.`);
      return;
    }

    setSelectedFiles((prevFiles) => ({
      ...prevFiles,
      [uploadType]: file.name,
    }));

    const formData = new FormData();
    formData.append(uploadOption.field, file);

    try {
      const response = await fetch(`http://127.0.0.1:8080${uploadOption.endpoint}`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Upload successful:", result);
      } else {
        console.error("Failed to upload file:", response.statusText);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleUploadClick = (type) => {
    currentUploadTypeRef.current = type;
    fileInputRef.current.click();
  };

  return (
    <div className="w-1/5 h-screen bg-gray-900 text-white p-10 flex flex-col">
      <h1 className="text-5xl font-bold mb-10">HOREG 2.0</h1>

      <div className="bg-gray-800 p-4 rounded mt-10 mb-15">
        <h3 className="text-lg font-bold mb-3">Upload Options</h3>

        <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" />

        <div className="flex space-x-2 mb-2">
          <button onClick={() => handleUploadClick("Audio")} className="flex-1 px-4 py-2 bg-green-700 text-white rounded-lg hover:bg-green-800">
            Audio
          </button>
          <button onClick={() => handleUploadClick("Image")} className="flex-1 px-4 py-2 bg-green-700 text-white rounded-lg hover:bg-green-800">
            Image
          </button>
        </div>

        <button className="w-full px-4 py-2 bg-white text-black font-bold rounded-lg hover:bg-green-900 hover:text-white mb-2">Search</button>
      </div>

      <ul className="list-none space-y-4 mb-10 mt-20">
        {uploadOptions
          .filter((option) => option.type !== "Audio" && option.type !== "Image")
          .map((option) => (
            <li key={option.type}>
              <button onClick={() => handleUploadClick(option.type)} className="w-full text-center px-4 py-2 rounded bg-gray-800 hover:bg-gray-700">
                {option.type}
              </button>
            </li>
          ))}
      </ul>

      <div className="grid grid-cols-[30%_5%_65%] gap-2">
        <p className="text-lg font-bold">Audio</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Audio}</p>
        <p className="text-lg font-bold">Image</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Image}</p>
        <p className="text-lg font-bold">Audios</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Audios}</p>
        <p className="text-lg font-bold">Images</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Images}</p>
        <p className="text-lg font-bold">Mapper</p>
        <p className="text-lg font-bold">:</p>
        <p className="text-lg font-bold">{selectedFiles.Mapper}</p>
      </div>
    </div>
  );
};

export default Sidebar;
