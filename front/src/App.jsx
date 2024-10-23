import './App.css'

import { Route, Routes } from 'react-router-dom';

import HomePage from './page/HomePage/HomePage';
import CreatePageDevice from './page/CreatePageDevice/CreatePageDevice';
import LoginPage from './page/LoginPage/LoginPage';
import RegistrationPage from './page/RegistrationPage/RegistrationPage';
import PageOfDevice from './page/PageOfDevice/PageOfDevice';

const App = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/create-device" element={<CreatePageDevice />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="/device/:id" element={<PageOfDevice />} />
      </Routes>
    </>
  );
};

export default App;