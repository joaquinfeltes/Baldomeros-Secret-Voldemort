const loginReducer = (
  state = { token: 0, logged_in: false, username: "", id: 0 },
  action
) => {
  switch (action.type) {
    case "LOGIN":
      if (action.payload.token === 145)
        return {
          token: action.payload.token,
          logged_in: true,
          username: action.payload.username,
          id: action.payload.id,
        };
      else return state;
    case "LOGOUT":
      return { token: 0, logged_in: false, username: "", id: 0 };
    default:
      return state;
  }
};
export default loginReducer;
