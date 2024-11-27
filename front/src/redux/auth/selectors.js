// export const selectUser = (state) => state.auth.user;
// export const selectIsLoggedIn = (state) => state.auth.isLoggedIn;
// export const selectIsLoading = (state) => state.auth.isLoading;
// export const selectError = (state) => state.auth.error;
// export const selectCsrfToken = (state) => state.auth.csrfToken;

export const selectUser = (state) => state.auth.user;
export const selectIsLoading = (state) => state.auth.isLoading;
export const selectError = (state) => state.auth.error;
export const selectIsLoggedIn = (state) => state.auth.isLoggedIn;
export const selectUserDataIsRefreshing = (state) => state.auth.isRefreshing;
export const selectUserDataToken = (state) => state.auth.token;
