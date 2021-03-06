import React from "react";
import { Provider } from "react-redux";
import Enzyme, { shallow, mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import Match from "../components/Match";
import reducers from "../reducers/index";
import { MemoryRouter, Route } from "react-router-dom";

Enzyme.configure({ adapter: new Adapter() });

describe("Match Interface", () => {
  const store = createStore(reducers);
  function wrap() {
    return mount(
      <Provider store={store}>
        <MemoryRouter initialEntries={[`/match/1`]}>
          <Route path="/match/:id" component={Match} />
        </MemoryRouter>
      </Provider>
    );
  }

  it("should show if you didn't join the game", () => {
    store.getState().match = { name: "Game 1", id: 2, hostName: "Tom Riddle" };
    const wrapper = wrap();
    const title = wrapper.find("div div");
    expect(title.text()).toBe(" You didn't join this game ");
  });

  it("Should show correct match name", () => {
    store.getState().match = { name: "Game 1", id: 1, hostName: "Tom Riddle" };
    const wrapper = wrap();
    const matchName = wrapper.find("div div div div h1");
    expect(matchName.at(0).text()).toBe(
      " " + store.getState().match.name + " "
    );
  });

  it("Should show correct match id", () => {
    store.getState().match = { name: "Game 1", id: 1, hostName: "Tom Riddle" };
    const wrapper = wrap();
    const matchId = wrapper.find("div div h4");
    expect(matchId.at(0).text()).toBe(
      " Game id : " + store.getState().match.id + " "
    );
  });
});
