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
      <section className="section">
        {pagesRequest.loading ? (
          <LoadSpinner />
        ) : pagesRequest.error ? (
          <div>{pagesRequest.error}</div>
        ) : (
          pagesRequest.payload.map(pageInfo => (
            <PageResult key={pageInfo.url} pageInfo={pageInfo}></PageResult>
          ))
        )}
      </section>
    </>
  );
}

export default App;
