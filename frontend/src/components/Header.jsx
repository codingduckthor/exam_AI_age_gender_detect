import "./Header.css";

function Header({ username }) {
  return (
    <header>
      <h2>AI Age Detection</h2>

      <div>Logged as: {username}</div>
    </header>
  );
}

export default Header;
