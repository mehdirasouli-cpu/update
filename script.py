from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import hashlib
import re
from pathlib import Path

# Research Parameters
primary_sample_count = 900
secondary_sample_count = 99
max_samples_per_dataset = 999

# Academic Data Sources for Network Protocol Research
primary_data_source = "https://t.me/s/ConfigsHUB"
secondary_data_sources = [
    'https://t.me/s/sinavm',
    'https://t.me/s/prrofile_purple',
    'https://t.me/s/V2RayNgTE',
    'https://t.me/s/MARAMBASHI',
    
]

# Research output directory
research_output = Path("output")
research_output.mkdir(exist_ok=True)

# Duplicate detection system
processed_samples_file = research_output / "processed_samples.txt"
processed_samples = set()
if processed_samples_file.exists():
    with open(processed_samples_file, "r", encoding="utf-8") as f:
        processed_samples = set(line.strip() for line in f if line.strip())

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Network protocol pattern matching for research
network_protocol_pattern = r"(?:vless|vmess|trojan|ss|ssr|tuic|hysteria)://[^\s]+"

def collect_research_samples(data_source_url, max_samples):
    driver.get(data_source_url)
    time.sleep(1)
    scroll_count = 0
    max_scrolls = 500
    collected_samples = []
    processed_messages = set()
    
    print(f"Collecting samples from {data_source_url}...")

    while len(collected_samples) < max_samples and scroll_count < max_scrolls:
        messages = driver.find_elements(By.CLASS_NAME, "tgme_widget_message_text")
        new_messages_found = False
        
        for msg in messages:
       
            msg_id = msg.get_attribute('outerHTML')[:400]
            
            if msg_id in processed_messages:
                continue
                
            processed_messages.add(msg_id)
            new_messages_found = True
            
            content = msg.text.strip()
            if not content:
                continue
                
        
            protocol_samples = re.findall(network_protocol_pattern, content, flags=re.IGNORECASE)
            
            for sample in protocol_samples:
            
                sample_hash = hashlib.sha256(sample.encode("utf-8")).hexdigest()

                if sample_hash not in processed_samples:
                    protocol_type = sample.split("://")[0].lower()
                    processed_samples.add(sample_hash)
                    collected_samples.append((protocol_type, sample))
                    
                    if len(collected_samples) >= max_samples:
                        print(f"Reached target of {max_samples} samples")
                        return collected_samples


        if not new_messages_found and scroll_count > 5:
            print("No new messages found, stopping collection...")
            break


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        scroll_count += 1
        
        if scroll_count % 10 == 0:
            print(f"Scroll {scroll_count}, collected {len(collected_samples)} samples")

    print(f"Finished collecting from {data_source_url}: {len(collected_samples)} samples found")
    return collected_samples

def optimize_dataset(file_path, max_entries):
    """Optimize dataset size by keeping only the most recent entries"""
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            entries = [line.strip() for line in f if line.strip()]
        if len(entries) > max_entries:
            entries = entries[-max_entries:]
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(entries) + "\n")

# Research Data Collection Process
print("Initiating research data collection...")
print(f"Target: {primary_sample_count} from primary source, {secondary_sample_count} total from {len(secondary_data_sources)} secondary sources")

start_time = time.time()
primary_samples = collect_research_samples(primary_data_source, primary_sample_count)
primary_time = time.time() - start_time
print(f"Primary source collection completed in {primary_time:.1f} seconds")

secondary_samples = []
for i, source in enumerate(secondary_data_sources, 1):
    if len(secondary_samples) >= secondary_sample_count:
        break
    remaining_capacity = secondary_sample_count - len(secondary_samples)
    print(f"\nCollecting from secondary source {i}/{len(secondary_data_sources)}: {source}")
    source_start = time.time()
    source_samples = collect_research_samples(source, remaining_capacity)
    source_time = time.time() - source_start
    print(f"Secondary source {i} completed in {source_time:.1f} seconds, collected {len(source_samples)} samples")
    secondary_samples.extend(source_samples)

driver.quit()
total_time = time.time() - start_time
print(f"\nTotal data collection completed in {total_time:.1f} seconds")

research_dataset = primary_samples + secondary_samples
print(f"Total research samples collected: {len(research_dataset)}")

if research_dataset:
    # Save comprehensive dataset
    comprehensive_dataset_path = research_output / "all_Mehdi_Rasouli_Samples.txt"
    with open(comprehensive_dataset_path, "a", encoding="utf-8") as f:
        for _, sample in research_dataset:
            f.write(sample + "\n")
    optimize_dataset(comprehensive_dataset_path, max_samples_per_dataset)

    # Categorize by protocol type
    protocol_categories = {}
    for protocol_type, sample in research_dataset:
        protocol_categories.setdefault(protocol_type, []).append(sample)

    for protocol_type, samples in protocol_categories.items():
        protocol_dataset_path = research_output / f"{protocol_type}_Mehdi_Rasouli_Samples.txt"
        with open(protocol_dataset_path, "a", encoding="utf-8") as f:
            for sample in samples:
                f.write(sample + "\n")
        optimize_dataset(protocol_dataset_path, max_samples_per_dataset)

    # Update processed samples registry
    with open(processed_samples_file, "a", encoding="utf-8") as f:
        for _, sample in research_dataset:
            sample_hash = hashlib.sha256(sample.encode("utf-8")).hexdigest()
            f.write(sample_hash + "\n")

    print(f"Research complete: {len(primary_samples)} primary + {len(secondary_samples)} secondary samples archived.")
else:
    print("No new research samples identified in this collection cycle.")


