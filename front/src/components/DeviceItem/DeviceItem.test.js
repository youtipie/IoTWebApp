// import { render } from "@testing-library/react";
// import { BrowserRouter } from "react-router-dom";
// import DeviceItem from "./DeviceItem.jsx";

// const mockDeviceActive = { id: "1", name: "Smart Lamp", status: "active" };
// const mockDeviceInactive = { id: "2", name: "Smart Fan", status: "inactive" };

// describe("DeviceItem component", () => {
//   test("renders the device name and state for active device", () => {
//     render(
//       <BrowserRouter>
//         <DeviceItem device={mockDeviceActive} />
//       </BrowserRouter>
//     );

//     expect(screen.getByText("Smart Lamp State:")).toBeInTheDocument();
//     const statusElement = screen.getByText("active");
//     expect(statusElement).toBeInTheDocument();
//     expect(statusElement).toHaveStyle("color: green");
//   });

//   test("renders the device name and state for inactive device", () => {
//     render(
//       <BrowserRouter>
//         <DeviceItem device={mockDeviceInactive} />
//       </BrowserRouter>
//     );

//     expect(screen.getByText("Smart Fan State:")).toBeInTheDocument();
//     const statusElement = screen.getByText("inactive");
//     expect(statusElement).toBeInTheDocument();
//     expect(statusElement).toHaveStyle("color: red");
//   });

//   test("renders a link with the correct URL", () => {
//     render(
//       <BrowserRouter>
//         <DeviceItem device={mockDeviceActive} />
//       </BrowserRouter>
//     );

//     const linkElement = screen.getByRole("link", { name: /Smart Lamp State:/ });
//     expect(linkElement).toHaveAttribute("href", "/device/1");
//   });
// });
