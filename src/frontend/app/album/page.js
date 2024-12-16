import SongList from "../Components/SongList";

const AlbumPage = () => {
  return (
    <div className="p-5">
      <h1 className="text-2xl font-bold mb-4">Album</h1>
      <SongList fetchUrl="http://127.0.0.1:8080/music/result/music.json" />
    </div>
  );
};

export default AlbumPage;
