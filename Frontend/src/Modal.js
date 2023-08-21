import React from "react";
import Login from "./components/login/loginForm";
import SignUp from "./components/signup/signupForm";
import Homepage from "./components/homepage/homepage"

// export default function Modal() {
//   const [showModal, setShowModal] = React.useState(false);
//   return (
//     <>
//       <button
//         className="bg-[#FFD400] text-black active:bg-pink-600 font-bold uppercase text-sm px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
//         type="button"
//         onClick={() => setShowModal(true)}
//       >
//         Login
//       </button>
//       {showModal ? (
//         <>
//           <div className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
//             <div className="relative w-auto my-6 mx-auto max-w-3xl">
//               {/*content*/}
//               <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
//                 {/*body*/}
//                 <div className="flex items-start justify-between p-5">
//                   <button
//                     className="absolute top-1 right-1 text-white bg-[#242424] font-bold px-4 py-2 text-sm mr-1 mb-1 transition-all duration-150 rounded-full uppercase"
//                     type="button"
//                     onClick={() => setShowModal(false)}
//                   >
//                     x
//                   </button>
//                 </div>
//                 <div>
//                   {/* <Login></Login> */}
//                   {/* <SignUp></SignUp> */}
//                 <Homepage></Homepage>
//                 </div>
//               </div>
//             </div>
//           </div>
//           <div className="opacity-75 fixed inset-0 z-40 bg-black"></div>
//         </>
//       ) : null}
//     </>
//   );
// }
