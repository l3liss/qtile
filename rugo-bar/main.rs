use std::io::{BufRead, BufReader};
use std::net::TcpStream;
use std::thread;
use std::time::Duration;
use x11rb::connection::Connection;
use x11rb::protocol::xproto::*;
use x11rb::rust_connection::RustConnection;
use tray_item::TrayItem;

fn create_x11_bar(conn: &RustConnection, screen_num: usize) -> u32 {
    let screen = &conn.setup().roots[screen_num];

    // Create window for the bar
    let win = conn.generate_id().unwrap();
    conn.send_request(&CreateWindow {
        depth: 0,
        wid: win,
        parent: screen.root,
        x: 0,
        y: 0,
        width: screen.width_in_pixels,
        height: 30, // 30px height bar
        border_width: 0,
        class: WindowClass::INPUT_OUTPUT,
        visual: screen.root_visual,
        value_list: &CreateWindowAux::default(),
    });

    // Set _NET_WM_WINDOW_TYPE to DOCK
    let dock_atom = conn.intern_atom(false, b"_NET_WM_WINDOW_TYPE_DOCK").unwrap();
    conn.change_property8(
        PropMode::REPLACE,
        win,
        dock_atom.reply().unwrap().atom,
        AtomEnum::CARDINAL,
        &[1],
    );

    // Reserve space (_NET_WM_STRUT_PARTIAL)
    let strut: [u32; 12] = [0, 0, 0, 30, 0, 0, 0, 0, 0, screen.width_in_pixels, 0, 0];
    conn.change_property32(
        PropMode::REPLACE,
        win,
        dock_atom.reply().unwrap().atom,
        AtomEnum::CARDINAL,
        &strut,
    );

    // Map window
    conn.map_window(win);
    conn.flush();

    win
}

fn connect_to_go_backend() {
    // Try connecting to Go backend
    match TcpStream::connect("127.0.0.1:8080") {
        Ok(stream) => {
            let reader = BufReader::new(stream);
            for line in reader.lines() {
                if let Ok(json) = line {
                    let data: serde_json::Value = serde_json::from_str(&json).unwrap();
                    println!(
                        "CPU: {}% | RAM: {} MB | Net: {} KB",
                        data["cpu"], data["ram"], data["net"]
                    );
                }
            }
        }
        Err(err) => {
            eprintln!("Failed to connect to Go backend: {}", err);
        }
    }
}

fn main() {
    let (conn, screen_num) = x11rb::connect(None).unwrap();
    let _win = create_x11_bar(&conn, screen_num);

    // Create system tray
    let mut tray = TrayItem::new("Rust Bar", "icon-name").unwrap();
    tray.add_label("System Tray").unwrap();

    // Spawn Go connection in a separate thread
    thread::spawn(connect_to_go_backend);

    // Keep running
    loop {
        thread::sleep(Duration::from_secs(1));
    }
}
