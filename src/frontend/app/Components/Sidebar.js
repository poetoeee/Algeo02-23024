"use client";
import { useState, useRef } from "react";
import { usePathname, useRouter } from "next/navigation";

const links = [
  { href: "/audios", label: "Audios" },
  { href: "/pictures", label: "Pictures" },
  { href: "/mapper", label: "Mapper" },
];

const Sidebar = () => {
  const router = useRouter();
  const pathname = usePathname();
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    alert(`File ${event.target.files[0].name} selected successfully!`);
  };

  const handleUploadClick = () => {
    // Simulate clicking the hidden file input
    fileInputRef.current.click();
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }
    alert(`File ${selectedFile.name} uploaded successfully!`);
    setSelectedFile(null); // Reset file after upload
  };

  const handleNavigation = (href) => {
    router.push(href);
  };

  return (
    <div className="w-1/5 h-screen bg-gray-900 text-white p-10 flex flex-col">
      <h1 className="text-5xl font-bold mb-10">HOREG 2.0</h1>
      <div className="bg-gray-800 p-4 rounded mt-10 mb-20">
        <h3 className="text-lg font-bold mb-3">Upload File</h3>

        <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" />

        <button onClick={handleUploadClick} className="w-full px-4 py-2 bg-green-700 text-white rounded hover:bg-green-800">
          Upload
        </button>

        {selectedFile && <p className="mt-3 text-sm text-gray-300">Selected: {selectedFile.name}</p>}
      </div>

      <ul className="list-none space-y-4 mb-10 mt-20">
        {links.map((link) => (
          <li key={link.href}>
            <button onClick={() => handleNavigation(link.href)} className={`w-full text-center px-4 py-2 rounded ${pathname === link.href ? "bg-gray-700" : "bg-gray-800 hover:bg-gray-700"}`}>
              {link.label}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
