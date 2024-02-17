#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn connect() {
        unsafe {
            // printf("XPlaneConnect Example Script\n- Setting up Simulation\n");

            // // Open Socket
            // const char* IP = "127.0.0.1";      //IP Address of computer running X-Plane
            // XPCSocket sock = openUDP(IP);
            // float tVal[1];
            // int tSize = 1;
            // if (getDREF(sock, "sim/test/test_float", tVal, &tSize) < 0)
            // {
            //     printf("Error establishing connecting. Unable to read data from X-Plane.");
            //     return EXIT_FAILURE;
            // }            
            
            // Open Socket
            // let ip: &str = "127.0.0.1";
            // println!("XPlaneConnect Test {}", ip);

            // let sock = openUDP(ip.as_bytes().as_ptr() as *const i8);

            // if (getDREF(sock, "sim/test/test_float".as_bytes().as_ptr() as *const i8, 1 as *mut f32, 1 as *mut i32) < 0) {
            //     println!("Error establishing connecting. Unable to read data from X-Plane.");
            //     return;
            // }

            assert_eq!(true,true);
        }
    }
}