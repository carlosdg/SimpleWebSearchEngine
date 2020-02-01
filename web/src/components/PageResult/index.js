import React from "react";
import "./index.css";

function useToggle(initialValue) {
  const [value, setValue] = React.useState(initialValue);
  const toggleValue = () => setValue(!value);

  return [value, toggleValue];
}

function PageResult(props) {
  const { url, title, text } = props.pageInfo;
  const [isModalActive, toggleModal] = useToggle(false);

  return (
    <>
      <div
        className="PageResult__container"
        tabIndex="0"
        role="link"
        onClick={toggleModal}
      >
        <p className="PageResult__url">{url}</p>
        <h3 className="PageResult__title">{title}</h3>
        <p className="PageResult__description">
          {text.substring(0, 500) + " ..."}
        </p>

        <div className={"modal" + (isModalActive ? " is-active" : "")}>
          <div className="modal-background"></div>
          <div className="modal-card">
            <header className="modal-card-head">
              <p className="modal-card-title">{title}</p>
              <button
                className="delete"
                aria-label="close"
                onClick={toggleModal}
              ></button>
            </header>
            <section className="modal-card-body">{text}</section>
          </div>
        </div>
      </div>
      <hr />
    </>
  );
}

export default PageResult;
