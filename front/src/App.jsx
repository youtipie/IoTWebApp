import './App.css'

import { Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';

import HomePage from './page/HomePage/HomePage';
import CreatePageDevice from './page/CreatePageDevice/CreatePageDevice';
import LoginPage from './page/LoginPage/LoginPage';
import RegistrationPage from './page/RegistrationPage/RegistrationPage';
import PageOfDevice from './page/PageOfDevice/PageOfDevice';
import DeviceListPage from './page/DeviceListPage/DeviceListPage';
import RestrictedRoute from './components/RestrictedRoute/RestrictedRoute';
import PrivateRoute from './components/PrivateRoute/PrivateRoute';
import Layout from './components/Layout/Layout';




const App = () => {

  return (
    <>
      <Layout>
        <Suspense fallback={<div>Loading...</div>}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<RestrictedRoute component={<LoginPage />} />} />
            <Route path="/register" element={<RestrictedRoute component={<RegistrationPage />} />} />
            <Route path="/device-list" element={<PrivateRoute component={<DeviceListPage />} />} />
            <Route path="/create-device" element={<PrivateRoute component={<CreatePageDevice />} />} />
            <Route path="/device/:id" element={<PrivateRoute component={<PageOfDevice />} />} />
          </Routes>
        </Suspense>
      </Layout>
    </>
  );
};

export default App;