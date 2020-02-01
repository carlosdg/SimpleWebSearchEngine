import React from "react";
import SearchBar from "../SearchBar";
import { fetchWebPages } from "./fetchWebPages";
import LoadSpinner from "../LoadSpinner";
import PageResult from "../PageResult";

function App() {
  const [pagesRequest, setPagesRequest] = React.useState({
    loading: false,
    payload: [],
    error: false
  });

  const onUserInput = React.useCallback(async filter => {
    setPagesRequest({ loading: true, payload: [], error: false });
    const response = await fetchWebPages(filter);
    setPagesRequest({ loading: false, ...response });
  }, []);

  return (
    <>
      <SearchBar onUserInput={onUserInput} />
      <section
        className="section"
        style={{ paddingTop: "0.5rem", paddingBottom: 0 }}
      >
        <div className="container">
          <div>About {pagesRequest.payload.length} results below</div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          {pagesRequest.loading ? (
            <LoadSpinner />
          ) : pagesRequest.error ? (
            <div>{pagesRequest.error}</div>
          ) : (
            <>
              {pagesRequest.payload.map(pageInfo => (
                <PageResult key={pageInfo.url} pageInfo={pageInfo}></PageResult>
              ))}
            </>
          )}
        </div>
      </section>
    </>
  );
}

export default App;
