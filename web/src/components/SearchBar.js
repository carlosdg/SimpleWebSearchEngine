import React from "react";

function SearchBar({ onUserInput }) {
  const [filter, setFilter] = React.useState("");

  return (
    <section className="section" style={{ paddingBottom: 0 }}>
      <div className="container">
        <div className="field has-addons">
          <div className="control is-expanded">
            <input
              className="input"
              type="text"
              placeholder="Find a web page"
              value={filter}
              onChange={e => setFilter(e.target.value)}
            />
          </div>
          <div className="control">
            <button
              type="submit"
              className="button is-info"
              onClick={() => onUserInput(filter)}
            >
              Search
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export default SearchBar;
