import axios from "axios";

    const baseUrl = "http://csci5308vm11.research.cs.dal.ca:8000/account";
    const baseUrl1 = "http://csci5308vm11.research.cs.dal.ca:8000/product";
    // const baseUrl = "http://localhost:5000"
    // const baseUrl1 = "http://localhost:5002"

    export const login = (credentials)=> {
        return axios.post(baseUrl+'/login',credentials);
     }

    export const health = ()=> {
    return axios.get(baseUrl+'/health');
    }

    export const signup = (user)=>{
        return axios.post(baseUrl+'/users/signup',user);
    }

    export const verify_email = (otp_verification)=>{
        return axios.post(baseUrl+'/users/verify_email',otp_verification);
    }

    export const selling_post = (formdata)=>{
        const token = localStorage.getItem('token');
        return axios.post(baseUrl1+'/products/addProduct',formdata,
        {
            headers: {
              Authorization: token
            }
          });
    }

    export const getting_allProducts = ()=>{
        const token = localStorage.getItem('token');
        return axios.get(baseUrl1+'/products/getProducts',
        {
            headers: {
              Authorization: token
            }
          });
    }

    export const readImages = (p_id)=> {
        const token = localStorage.getItem('token');
        return axios.get(baseUrl1+'/products/getProduct/readImages/'+p_id,
        {
            headers: {
              Authorization: token
            }
          });
        }

    export const getting_myProducts = ()=>{
        const token = localStorage.getItem('token');
        return axios.get(baseUrl1+'/products/myProducts',
        {
            headers: {
                Authorization: token
            }
            });
    }

    export const delete_post = (product_id) => {
        const token = localStorage.getItem('token');
        return axios.post(
            baseUrl1 + '/products/deleteProduct/' + product_id,
          {},
          {
            headers: {
              Authorization: token
            }
          }
        );
      }

    export const getUser = ()=>{
    const token = localStorage.getItem('token');
    return axios.get(baseUrl+'/users/get_user',
    {
        headers: {
            Authorization: 'Bearer '+ token
        }
        });
    }

    export const getSeller = (user_id)=>{
        const token = localStorage.getItem('token');
        return axios.get(baseUrl+'/users/get_seller/'+user_id,
        {
            headers: {
                Authorization: 'Bearer '+ token
            }
            });
        }