import HomePage from "./components/homepage/homepage";
import WelcomePage from "./components/welcome/welcome";
import Login from "./components/login/loginForm";
import SignUp from "./components/signup/signupForm";
import Sell from "./components/sell/sell";
import Buying from "./components/buying/buying";
import Product_Details from "./components/product_details/product_details";
import MyProducts from "./components/my_products/my_products";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import axios from 'axios';
import UserDetails from "./components/userprofile/user";

function App() {
  axios.interceptors.request.use(config => {
        config.headers['Origin'] = 'http://localhost:3001';
        return config;
      });
  return (
 
    <div className="flex w-full h-screen">
      <div className="w-full flex items-center justify-center">
      <BrowserRouter>
      <Routes>
      <Route exact path="/" element={<HomePage />} />
      <Route path="/WelcomePage" element={<WelcomePage />} />
      <Route path="/Login" element={<Login />} />
      <Route path="/SignUp" element={<SignUp />} />
      <Route path="/Sell" element={<Sell />} />
      <Route path="/Buying" element={<Buying />} />
      <Route path="/Product_Details" element={<Product_Details />} />
      <Route path="/UserDetails" element={<UserDetails />} />
      <Route path="/MyProducts" element={<MyProducts />} />
      </Routes>
    </BrowserRouter>

      </div>
    </div>

  );
}

export default App;
