import * as React from "react";
import { Link } from 'react-router-dom';
import logo from "../../assets/logo.png";
import { useState } from "react";
import ImageUploading from "react-images-uploading";
import axios from 'axios';
import { selling_post } from "../../services/api-service";
import { useNavigate } from "react-router-dom";

export default function Sell() {
  const [images, setImages] = React.useState([]);
  const maxNumber = 3;
  const navigate = useNavigate();

  const onChange = (imageList, addUpdateIndex) => {
    // data for submit
    console.log(imageList, addUpdateIndex);
    setImages(imageList);
  };

  // let seller = {
  //   title: '',
  //   description: '',
  //   price: '',
  //   address: '',
  //   category:'',
  //   status:''
  // };

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [address, setAddress] = useState('');
  const [category, setCategory] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const form = event.target;
  
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('address', address);
    formData.append('category', category);
    formData.append('status', 'New');
    formData.append('titImage', images[0].file);
    formData.append('secImage', images[1].file);
    formData.append('terImage', images[2].file);
  
    await selling_post(formData)
    .then((response) => {
      console.log(response.data);
      navigate('/WelcomePage');
    })
    .catch((error) => {
      console.log(error);
    });
  }

  return (
    
    <div className="bg-white w-full h-screen pt-4">

      <img src={logo} className="App-logo" alt="logo" />
      <h2 className="text-2x text-center pb-4 pl-4 font-extrabold">Student Marketplace </h2>
      <hr/>

      <div className="user_nav">
        <div class="relative inline-block">
        <Link to="/WelcomePage"><b>&nbsp;&nbsp;Home&nbsp;&nbsp;</b></Link>
        </div>
      </div>

      <div className="pl-5">
        <p className="font-bold text-2xl pb-1 text-black mt-2">
        <h2 className="text-2xl font-semibold">Sell your stuff!</h2>
        </p>
      </div>
      
      <div className="bg-white px-popup3 pb-24">

        <h2 className="text-xl font-semibold text-gray-500">Post your Ad in minutes!</h2>
        
        <div className="mt-6">
          <div>
            <label className="text-lg font-medium">Ad Title</label>
            <input
              className="w-full border-2 border-gray-200 rounded-xl p-3 mt-1 bg-transparent italic"
              placeholder="iPhone 14 Pro"
              id="title"
              value={title} 
              onChange={e => setTitle(e.target.value)}
            />
          </div>
          <div className="mt-3">
            <label className="text-lg font-medium">Ad Description</label>
            <div className="w-full flex flex-col border-2 border-gray-200 rounded-xl p-3 mt-1 bg-transparent">
              <textarea
                className=" italic rounded-md"
                placeholder="iPhone 14 Pro for sale! Space Black, 256 GB."
                id="description"
                value={description} 
                onChange={e => setDescription(e.target.value)}
              ></textarea>
            </div>
          </div>
          <div className="mt-3">
            <label className="text-lg font-medium">Price</label>
            <input
              maxLength={5}
              className="w-full border-2 border-gray-200 rounded-xl p-3 mt-1 bg-transparent italic"
              placeholder="$ 1300"
              id="price"
              value={price} 
              onChange={e => setPrice(e.target.value)}
            />
          </div>
          <div className="mt-3">
            <label className="text-lg font-medium">Address</label>
            <input
              className="w-full border-2 border-gray-200 rounded-xl p-3 mt-1 bg-transparent italic"
              placeholder="$ 6230 Coburg Rd, Halifax, NS B3H 1Z7"
              id="address"
              value={address} 
              onChange={e => setAddress(e.target.value)}
            />
          </div>
          <div className="mt-3">
            <label className="text-lg font-medium">Category</label>
            <select
                className="w-full border-2 border-gray-200 rounded-xl p-3 mt-1 bg-transparent italic"
                id="category"
                value={category}
                onChange={e => setCategory(e.target.value)}
                required
              >
                <option value="">-- Select a category --</option>
                <option value="Electronics">Electronics</option>
                <option value="Books">Books</option>
                <option value="Furniture">Furniture</option>
                <option value="Clothing">Clothing</option>
                <option value="Musical Instruments">Musical Instruments</option>
                <option value="Sports Equipments">Sports Equipments</option>
                <option value="Others" selected>Others</option>
              </select>
          </div>

          <div className="px-k">
            <ImageUploading
              multiple
              value={images}
              onChange={onChange}
              maxNumber={maxNumber}
              dataURLKey="data_url"
            >
              {({
                imageList,
                onImageUpload,
                onImageRemoveAll,
                onImageUpdate,
                onImageRemove,
                isDragging,
                dragProps,
              }) => (
                // write your building UI
                <div className="w-full gap-y-4">
                  <div className="mt-4 mr-5">
                    <button
                      className="p-3 active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-3 rounded-xl bg-[#FFD400] text-black text-text-lg font-semibold"
                      style={isDragging ? { color: "red" } : undefined}
                      onClick={onImageUpload}
                      {...dragProps}
                    >
                      Upload Images
                    </button>
                    &nbsp;
                    <button
                      className="p-3 ml-4 active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-3 rounded-xl bg-[#FFD400] text-black text-text-lg font-semibold"
                      onClick={onImageRemoveAll}
                    >
                      Remove all images
                    </button>
                    {imageList.map((image, index) => (
                      <div key={index} className="image-item">
                        <img
                          className="m-2 rounded-md"
                          src={image["data_url"]}
                          alt=""
                          width="500"
                        />
                        <div className="image-item__btn-wrapper">
                          <button
                            className="p-3 active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-2 rounded-xl bg-[#FFCC00] text-black text-text-lg font-semibold"
                            onClick={() => onImageUpdate(index)}
                          >
                            Update
                          </button>
                          <button
                            className="p-3 ml-4 active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-2 rounded-xl bg-[#FFCC00] text-black text-text-lg font-semibold"
                            onClick={() => onImageRemove(index)}
                          >
                            Remove
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </ImageUploading>
          </div>
          <div className="mt-8 flex flex-col gap-y-4">
            <button
              type="submit" 
              onClick={handleSubmit}
              size="lg"
              className="active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-3 rounded-xl bg-[#FFD400] text-black text-text-lg font-bold"
            >
              Post Ad
            </button>
          </div>
        </div>
      </div>

      <hr/>
      <div className="footer">
        <div className='footer_text1'>
          <b>Dalhousie University</b><br/>Halifax, Nova Scotia, Canada B3H 4R2
        </div>

        <div className='footer_text2'>
          <Link className="footer_links" to="">&nbsp;About&nbsp;</Link>
          <Link className="footer_links" to="">&nbsp;Contact Us&nbsp;</Link>         
        </div>
      </div>
    </div>
  );
}