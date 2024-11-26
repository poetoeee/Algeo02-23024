"use client";
import { usePathname, useRouter } from "next/navigation"; // Import hooks

const links = [
  {
    href: "/upload",
    label: "Upload",
  },
  {
    href: "/audios",
    label: "Audios",
  },
  {
    href: "/pictures",
    label: "Pictures",
  },
  {
    href: "/mapper",
    label: "Mapper",
  },
];

const Sidebar = () => {
  const router = useRouter();
  const pathname = usePathname();

  const handleNavigation = (href) => {
    router.push(href);
  };

  return (
    <div className="w-70 h-screen bg-gray-900 text-white p-20">
      <ul className="list-none flex flex-col text-lg space-y-6">
        {links.map((link) => (
          <li key={link.href} className="relative">
            <button
              onClick={() => handleNavigation(link.href)}
              className={`px-10 w-full text-center cursor-pointer font-bold p-3 rounded transition-colors duration-150 ${pathname === link.href ? "bg-gray-700 text-white" : "bg-gray-800 hover:bg-gray-700"}`}
            >
              {pathname === link.href && <span className="absolute left-[-16px] top-0 h-full w-2 bg-blue-500 rounded-r"></span>}
              {link.label}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
